import asyncio
import random
import textwrap
import time
import apprise
from curl_cffi import requests
from curl_cffi.requests.exceptions import (
    ProxyError, 
    ConnectTimeout as ConnectTimeoutCffi, 
    ConnectionError as ConnectionErrorCffi,
    Timeout as TimeoutErrorCffi
)
from curl_cffi.requests import AsyncSession
from proxy_rotator_toolkit.custom_exceptions import NoProxiesAvailable #, ProxyRetriesExceeded, CantGetProxiesFromAPI
from proxy_rotator_toolkit.notification import SlackNotifier


class ProxyMiddleman:
    BAD_RESPONSE_CODE = {401, 403, 451, 429}
    
    def __init__(
            self, 
            connectors_ids: list[str], 
            slack_webhook_url: str,
            get_proxy_url: str,
            number_of_retries: int = 5, 
            backoff_time: int = 10, 
            exponential_backoff: bool = True,
            use_semaphore: bool = False,
            request_per_proxy: int = 1,
            send_alert_after_unexpected_errors: int = 5,
            bad_response_code: set = None,
            notifier: SlackNotifier = None,
            proxy_not_working_fails: int = 3,
        ):
        """
        Initializes the ProxyMiddleman instance with configuration parameters.

        :param connectors_ids: The IDs of the connectors to use.
        :param number_of_retries: Number of retries for proxy requests.
        :param backoff_time: Base time for backoff in seconds.
        :param exponential_backoff: Boolean indicating if exponential backoff should be used.
        :param slack_webhook_url: The URL of the Slack webhook to use for notifications.
        :param use_semaphore: Boolean indicating if semaphore should be used.
        :param request_per_proxy: Number of requests per proxy.
        :param send_alert_after_unexpected_errors: Number of unexpected errors after which an alert should be sent.
        :param get_proxy_url: Endpoint url
        :param notifier: SlackNotifier class instance
        """
        self.connectors = {}  # Save connectors as {connector_id: proxies}
        self.number_of_retries = number_of_retries
        self.backoff_time = backoff_time
        self.exponential_backoff = exponential_backoff
        self.get_proxy_url = get_proxy_url

        if bad_response_code:
            self.BAD_RESPONSE_CODE.update(bad_response_code)

        self.use_semaphore = use_semaphore
        self.request_per_proxy = request_per_proxy
        
        self.send_alert_after_unexpected_errors = send_alert_after_unexpected_errors
        self.notifier = notifier if notifier else SlackNotifier(slack_webhook_url)

        self.notification_title = "Middleman Proxy Info"
        self.proxy_not_working_fails = proxy_not_working_fails
        
        self.deleted_proxies = set()
        self.lock = asyncio.Lock()

        self.semaphores = {}
        for connector_id in connectors_ids:
            self.connectors[connector_id], semaphore_value = self._initialize_proxies_and_semaphore(connector_id)
            if semaphore_value:
                self.semaphores[connector_id] = asyncio.Semaphore(semaphore_value)

    def _fetch_proxies_data(self):
        """Requests proxy data from the API, retrying indefinitely until success."""
        last_notification_time = 0

        while True:
            try:
                response = requests.get(self.get_proxy_url)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                current_time = time.time()
                if current_time - last_notification_time >= 300:  # 5 minutes
                    self.notifier.notify(f"Cannot get proxies from API. Error: {e}. Sleeping for 5 minutes", title=self.notification_title, notify_type=apprise.NotifyType.WARNING)
                    last_notification_time = current_time

                time.sleep(self.backoff_time)
        # raise CantGetProxiesFromAPI(last_error)

    def _initialize_proxies_and_semaphore(self, connector_id):
        """
        Initializes a list of proxies for the specified connector_id.
        """
        data = self._fetch_proxies_data()

        for entry in data:
            if entry["connector_id"] == connector_id:
                proxies = entry["proxies"]
                break
        else:
            raise NoProxiesAvailable(connector_id)

        proxy_data = {
            proxy: {
                "unexpected_fails": 0,
                "proxy_not_working_fails": 0,
                "disabled_until": None,
                "added_at": time.time(),
                "request_count": 0,
            }
            for proxy in proxies
        }

        semaphore = len(proxies) * self.request_per_proxy if self.use_semaphore else None
        return proxy_data, semaphore

    def _find_new_proxies(self):
        """
        Checks and adds new proxies.
        """
        data = self._fetch_proxies_data()
        new_proxies_found = False

        for entry in data:
            connector_id = entry["connector_id"]
            if connector_id in self.connectors:
                existing_proxies = set(self.connectors[connector_id])
                new_proxies = set(entry["proxies"]) - existing_proxies - self.deleted_proxies

                if new_proxies:
                    new_proxies_found = True
                    self.connectors[connector_id].update({
                        proxy: {
                            "unexpected_fails": 0,
                            "proxy_not_working_fails": 0,
                            "disabled_until": None,
                            "added_at": time.time(),
                            "request_count": 0,
                        }
                        for proxy in new_proxies
                    })
                    self._recalculate_semaphore(connector_id)
                    self.notifier.notify(
                        f"New proxies ({len(new_proxies)}) were found for connector {entry.get('connector_name', connector_id)}",
                        title=self.notification_title
                    )
        return new_proxies_found
        
    async def _get_available_proxies(self, connector_id=None):
        current_time = time.time()
        available_proxies = {}

        connectors = (
            {connector_id: self.connectors[connector_id]}
            if connector_id and connector_id in self.connectors
            else self.connectors
        )

        for conn_id, proxies in connectors.items():
            filtered_proxies = [
                p for p, meta in proxies.items()
                if meta["disabled_until"] is None or meta["disabled_until"] < current_time
            ]
            if filtered_proxies:
                available_proxies[conn_id] = filtered_proxies

        return available_proxies

    async def _get_proxy(self):
        last_notification_time = 0

        async with self.lock:
            while True:
                available_proxies = await self._get_available_proxies()

                if available_proxies:
                    connector_id, proxies = random.choice(list(available_proxies.items()))
                    return connector_id, random.choice(proxies), self.semaphores.get(connector_id)
                
                if self._find_new_proxies():
                    continue

                current_time = time.time()
                if current_time - last_notification_time >= 300:  # 5 minutes
                    self.notifier.notify("No available proxies! Sleeping for 5 minutes...", title=self.notification_title, notify_type=apprise.NotifyType.WARNING)
                    last_notification_time = current_time

                await asyncio.sleep(30)

    async def _disable_proxy(self, connector_id, proxy, unexpected_error=False, proxy_not_working=False, response_text=None):
        """
        Disables a proxy for a given connector_id. If a proxy fails 3 times in a row, it gets removed.

        :param connector_id: The ID of the connector containing the proxy.
        :param proxy: The name of the proxy to disable.
        """
        if connector_id in self.connectors and proxy in self.connectors[connector_id]:
            if unexpected_error:
                self.connectors[connector_id][proxy]["unexpected_fails"] += 1
            elif proxy_not_working:
                self.connectors[connector_id][proxy]["proxy_not_working_fails"] += 1
            else:
                raise ValueError("unexpected_error or proxy_not_working must be True")

            # If the proxy breaks 3 times in a row, delete it
            if self.connectors[connector_id][proxy]["proxy_not_working_fails"] >= self.proxy_not_working_fails:
                self.notifier.notify(f"Proxy '{proxy}' removed after {self.proxy_not_working_fails} consecutive failures. Response text: {response_text}", title=self.notification_title, notify_type=apprise.NotifyType.WARNING)
                self.deleted_proxies.add(proxy)
                del self.connectors[connector_id][proxy]
                await self._recalculate_semaphore(connector_id)
            else:
                # Normal shutdown with backoff
                max_fails = max(self.connectors[connector_id][proxy]["unexpected_fails"], self.connectors[connector_id][proxy]["proxy_not_working_fails"])
                backoff = self.backoff_time * (2 ** max_fails) if self.exponential_backoff else self.backoff_time
                self.connectors[connector_id][proxy]["disabled_until"] = time.time() + backoff
 
    async def _get_semaphore(self):
        """
        :return: A semaphore for the availble_proxies_count * request_per_proxy.
        """
        _, _, semaphore = await self._get_proxy()
        return semaphore
    
    async def _recalculate_semaphore(self, connector_id: str):
        if not self.use_semaphore:
            return None

        all_proxies = self.connectors.get(connector_id, {})
        semaphore_value = len(all_proxies) * self.request_per_proxy

        if semaphore_value > 0:
            self.semaphores[connector_id] = asyncio.Semaphore(semaphore_value)
        else:
            self.notifier.notify(f"No proxies available for connector {connector_id}.", title=self.notification_title, notify_type=apprise.NotifyType.WARNING)

    async def _request(self, url, method="GET", **kwargs):
        """
        Sends an HTTP request using a proxy, with retries on failure.

        :param url: The URL to send the request to.
        :param method: The HTTP method to use (default is "GET").
        :param kwargs: Additional arguments to pass to the request.
        :return: The HTTP response object.
        :raises Exception: If all proxies fail after the specified number of retries.
        """
        last_error = None

        for _ in range(self.number_of_retries):
            connector_id, proxy, _ = await self._get_proxy()
            try:
                async with AsyncSession() as session:
                    response = await session.request(method, url, proxy=proxy, **kwargs)
                
                self.connectors[connector_id][proxy]["request_count"] += 1
                
                if response.status_code in self.BAD_RESPONSE_CODE:
                    await self._disable_proxy(connector_id, proxy, unexpected_error=True, response_text=response.text)
                    continue
                self.connectors[connector_id][proxy]["proxy_not_working_fails"] = 0
                return response
            except UnicodeDecodeError as unicode_error:
                last_error = unicode_error
                break
            except (TimeoutErrorCffi, ConnectionErrorCffi, ConnectTimeoutCffi) as connection_error:
                last_error = connection_error
                await asyncio.sleep(1)
            except ProxyError as proxy_error:
                last_error = proxy_error
                await self._disable_proxy(connector_id, proxy, proxy_not_working=True, response_text=last_error)
            except Exception as unexpected_error:
                last_error = unexpected_error
                await self._disable_proxy(connector_id, proxy, unexpected_error=True)

        shortened_kwargs = {
            key: textwrap.shorten(str(value), width=30, placeholder="...")
            for key, value in kwargs.items()
        }
        error = (
            f"Url - {url}\n"
            f"Method - {method}\n"
            f"Kwargs - {shortened_kwargs}\n"
            f"Type - {type(last_error)}\n"
            f"Msg - {last_error}"
        )
        self.notifier.notify(error, title=self.notification_title, notify_type=apprise.NotifyType.FAILURE)
        # raise ProxyRetriesExceeded(self.number_of_retries) 

    async def request(self, url, method="GET", **kwargs):
        """
        Sends an HTTP request using a proxy, with retries on failure.

        :param url: The URL to send the request to.
        :param method: The HTTP method to use (default is "GET").
        :param kwargs: Additional arguments to pass to the request.
        :return: The HTTP response object.
        :raises Exception: If all proxies fail after the specified number of retries.
        """

        if self.use_semaphore:
            semaphore = await self._get_semaphore()
            async with semaphore:
                return await self._request(url, method, **kwargs)
        else:
            return await self._request(url, method, **kwargs)

    def notify(self, message, notify_type=apprise.NotifyType.INFO):
        """
        Sends a notification with the given message.

        :param message: The message to include in the notification.
        :param notify_type: The type of the notification.
        """
        try:
            if self.apprise_obj:
                self.apprise_obj.notify(
                    body=message,
                    title=self.notification_title,
                    notify_type=notify_type
                )
            else:
                print("No apprise object found. Skipping notification")
        except Exception as e:
            print(f"Error sending notification: {e}")

    def get_proxy_stats(self):
        """
        Returns statistics for all proxies in all connectors.

        :return: A dictionary containing statistics for each proxy, including request count, lifetime, and fails.
        """
        return {
            connector_id: {
                proxy: {
                        "request_count": meta["request_count"],
                        "lifetime_minutes": round((time.time() - meta["added_at"]) / 60, 2),
                        "unexpected_fails": meta["unexpected_fails"],
                        "proxy_not_working_fails": meta["proxy_not_working_fails"],
                        "disabled_until": meta["disabled_until"]
                    }
                    for proxy, meta in proxies.items()
                }
                for connector_id, proxies in self.connectors.items()
            }
