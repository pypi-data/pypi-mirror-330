import time
from apprise import Apprise, NotifyType


class SlackNotifier:
    _instance = None

    def __new__(cls, slack_webhook_url: str):
        if not cls._instance:
            cls._instance = super(SlackNotifier, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, slack_webhook_url: str):
        if self._initialized:
            return
        
        self.apprise_obj = Apprise()
        self.apprise_obj.add(slack_webhook_url)
        self._initialized = True

    def notify(self, message, notify_type=NotifyType.INFO, title: str = "Notification", retry=3):
        print("Sending Slack notification...")
        for attempt in range(retry):
            try:
                if self.apprise_obj.notify(
                    body=message,
                    title=title,
                    notify_type=notify_type,
                ):
                    print("Notification sent successfully")
                    return
                else:
                    print("Notification failed, retrying...")
            except Exception as e:
                print(f"Error sending notification: {e}. Retrying...")
            
            if attempt < retry - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        print("Failed to send notification after retries.")


if __name__ == "__main__":
    slacknotifier = SlackNotifier("https://hooks.slack.com/services/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")
    slacknotifier.notify(message="test")