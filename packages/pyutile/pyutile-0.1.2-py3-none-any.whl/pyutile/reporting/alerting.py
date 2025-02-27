def send_alert(message: str):
    """
    Stub function for sending alerts to external monitoring services.
    In production, integrate with services like Slack, PagerDuty, or email notifications.
    """
    # For demonstration purposes, we'll simply print the alert.
    print("ALERT:", message)

def alert_sink(message):
    """
    Custom Loguru sink that sends an alert for ERROR and CRITICAL logs.
    The 'message' parameter is a Loguru Message object.
    """
    record = message.record
    formatted_message = f"{record['time']} - {record['level'].name}: {record['message']}"
    send_alert(formatted_message)