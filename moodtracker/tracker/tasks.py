from background_task import background
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

@background  # just decorate the function
def send_reminders():
    now = timezone.now()
    for user in User.objects.exclude(pushover_user_key__isnull=True)\
                             .exclude(pushover_app_token__isnull=True):
        interval = user.reminder_interval_hours
        if not interval:
            continue

        last_answer = user.answers.order_by('-created_at').first()
        if not last_answer or last_answer.created_at + timedelta(hours=interval) > now:
            continue

        if user.last_reminder_sent and user.last_reminder_sent + timedelta(hours=3) > now:
            continue

        payload = {
            'token': user.pushover_app_token,
            'user': user.pushover_user_key,
            'device': user.pushover_device_name,
            'message': "Hi there! You haven’t answered your questions in a bit—please take a moment now.",
        }
        try:
            resp = requests.post('https://api.pushover.net/1/messages.json', data=payload)
            resp.raise_for_status()
        except Exception as e:
            # replace with proper logging in production
            print(f"❌ Pushover failed for {user.username}: {e}")
            continue

        user.last_reminder_sent = now
        user.save(update_fields=['last_reminder_sent'])
