from background_task import background
from django.utils.timezone import now
from datetime import timedelta
from tracker.models import CustomUser, Answer
import requests

@background(schedule=60)
def send_reminder_notifications():
    for user in CustomUser.objects.exclude(pushover_user_key__isnull=True).exclude(pushover_user_key__exact=""):
        last_answer = Answer.objects.filter(user=user).order_by("-created_at").first()
        hours = user.reminder_interval_hours or 12

        should_send = False
        if not last_answer:
            should_send = True
        elif (now() - last_answer.created_at) > timedelta(hours=hours):
            should_send = True

        if should_send:
            send_pushover_message(user.pushover_user_key, f"Hi {user.username}, it's time to check in with MoodTracker!")

def send_pushover_message(user_key, message):
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": "YOUR_APP_API_TOKEN",
        "user": user_key,
        "message": message,
    })
