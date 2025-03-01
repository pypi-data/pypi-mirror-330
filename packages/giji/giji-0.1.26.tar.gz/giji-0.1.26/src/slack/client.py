from typing import Optional
import os
import requests
from urllib.parse import urlparse


class SlackClient:
    """Client for interacting with Slack API using Webhooks."""

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize Slack client with webhook URL from parameters or environment variable.
        
        Args:
            webhook_url: Slack Incoming Webhook URL. If not provided, will try to get from SLACK_WEBHOOK_URL env var.
        """
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError(
                "Slack webhook URL not found. Please provide it as parameter or set SLACK_WEBHOOK_URL environment variable."
            )
        
        # Validate webhook URL format
        parsed = urlparse(self.webhook_url)
        if not all([parsed.scheme, parsed.netloc]) or "hooks.slack.com" not in parsed.netloc:
            raise ValueError("Invalid Slack webhook URL format")

    def send_message(self, text: str, channel: Optional[str] = None) -> bool:
        """
        Send a message to Slack using webhook.
        
        Args:
            text: The message text to send
            channel: Ignored for webhooks as they are pre-configured to a specific channel
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            payload = {"text": text}
            response = requests.post(self.webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending message to Slack: {str(e)}")
            return False

    @classmethod
    def from_env(cls) -> "SlackClient":
        """Create a SlackClient instance using environment variables."""
        return cls() 