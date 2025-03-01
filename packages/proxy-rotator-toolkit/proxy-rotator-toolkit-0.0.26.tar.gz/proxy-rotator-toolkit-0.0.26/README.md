# How to use proxy-middleman module

1. Create a connectors in scrapoxy (<a>http://185.253.7.140:8890/projects/d1bfcfdc-5f71-4a7a-a83a-252d1f25de4a/connectors/view</a>)
2. Get the IDs of the created connectors (<a>http://185.253.7.140:8080/docs#/default/list_proxies_proxies_get</a>)
3. Install the module proxy-middleman.

```bash
pip install proxy-middleman
```

4. Import the class ProxyMiddleman from the module proxy-middleman.

```python
from proxy_rotator_toolkit.proxy_rotation import ProxyMiddleman
```

5. Create an instance of the ProxyMiddleman class.

```python
proxy_middleman = ProxyMiddleman(connectors_ids=[connector_id1, connector_id2, connector_id3])
```
- connectors_ids: The list of IDs of the connectors to use.
- number_of_retries: Number of retries for proxy requests. If the response returned with status 401/403/451/503, then the proxy will be changed, it will try to do it `number_of_retries` times
- backoff_time: Base time for backoff in seconds. If the response returned with status 401/403/451/503, then this proxy will no longer be used at least `backoff_time` seconds
- exponential_backoff: Boolean indicating if exponential backoff should be used. If True, increases the backoff time exponentially (2^fails * backoff_time).
- slack_webhook_url: The URL of the Slack webhook to use for notifications.
- use_semaphore: Boolean indicating if semaphore should be used. If True, then the number of requests per proxy will be limited by the semaphore.
- request_per_proxy: Number of requests per proxy.
- send_alert_after_unexpected_errors: Number of unexpected errors after which an alert should be sent.


### For example if `backoff_time = 10` and `exponential_backoff = True` then:
- 1st retry: 10 seconds
- 2nd retry: 20 seconds
- 3rd retry: 40 seconds
- 4th retry: 80 seconds
- 5th retry: 160 seconds
- 6th retry: 320 seconds
- 7th retry: 640 seconds
- 8th retry: 1280 seconds
- 9th retry: 2560 seconds

6. Use the `request` method to send requests to the target site.

```python
    try:
        response = await proxy_middleman.request("http://example.com")
        print(response.text)
    except Exception as e:
        print(e)
```
7. Check the stats of the proxies using the `get_proxy_stats` method.

```python
    stats = proxy_manager.get_proxy_stats()
    print(stats)
```

# How it works

Before sending a request, we look at which proxies are currently available. If there are no available proxies, a message will be sent to slack and the wait for the first available proxy will begin. After sending a request and receiving a response, the response status is checked, if it does not satisfy us (401, 403, 451, 503), then we disable this proxy for `backoff_time` seconds. And this will continue until a good response_status is returned or attempts equal to `number_of_retries` are over (in this case, a message will be sent to slack and an exception will be raised in the code).