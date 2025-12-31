import requests
from django.conf import settings

def send_onesignal_notification(message, player_ids=None, segments=None):
    """
    Send a push notification via OneSignal.

    :param message: The notification message.
    :param player_ids: List of player IDs to send to specific users.
    :param segments: List of segments (e.g., ["All"] for all users).
    """
    if not settings.ONESIGNAL_API_KEY or settings.ONESIGNAL_API_KEY == "your-api-key-here":
        print("OneSignal API key not set. Skipping notification.")
        return

    url = "https://onesignal.com/api/v1/notifications"
    headers = {
        "Authorization": f"Basic {settings.ONESIGNAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "app_id": settings.ONESIGNAL_APP_ID,
        "contents": {"en": message},
    }
    if player_ids:
        data["include_player_ids"] = player_ids
    elif segments:
        data["included_segments"] = segments
    else:
        data["included_segments"] = ["All"]

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification: {response.status_code} - {response.text}")