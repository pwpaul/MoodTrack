import logging
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
import requests

logger = logging.getLogger(__name__)
User = get_user_model()

def send_reminders():
    logger.info("🔥 Task send_reminders STARTED!")

    now = timezone.now()

    users = User.objects.exclude(pushover_user_key__isnull=True).exclude(pushover_app_token__isnull=True)
    logger.info(f"🔍 Found {users.count()} users eligible for reminder check.")

    for user in users:
        logger.info(f"👤 Checking user: {user.username}")

        interval = user.reminder_interval_hours
        if not interval:
            logger.info(f"⏭️ Skipping user {user.username} (no interval set)")
            continue

        last_answer = user.answer_set.order_by('-created_at').first()
        if not last_answer or last_answer.created_at + timedelta(hours=interval) > now:
            logger.info(f"⏭️ Skipping user {user.username} (answered recently or never)")
            continue

        if user.last_reminder_sent and user.last_reminder_sent + timedelta(hours=.25) > now:
            logger.info(f"⏭️ Skipping user {user.username} (recent reminder sent)")
            continue

        payload = {
            'token': user.pushover_app_token,
            'user': user.pushover_user_key,
            'device': user.pushover_device_name,
            'title': "AshleyTron2000: Mood Tracker Reminder",
            'message': f"{user.username}, You haven’t answered your questions in a bit—please take a moment now.",
            'url': "https://ashleytron2000.reallypaul.wtf",
            'url_title': "Ashelytron2000",
        }
        try:
            resp = requests.post('https://api.pushover.net/1/messages.json', data=payload)
            resp.raise_for_status()
            logger.info(f"✅ Pushover message sent for user: {user.username}")
        except Exception as e:
            logger.error(f"❌ Pushover failed for {user.username}: {e}")
            continue

        user.last_reminder_sent = now
        user.save(update_fields=['last_reminder_sent'])
        logger.info(f"💾 Updated last_reminder_sent for {user.username}")

    logger.info("🎉 Task send_reminders COMPLETED!")
