from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_q.models import Schedule
import logging

logger = logging.getLogger(__name__)

@receiver(post_migrate)
def schedule_send_reminders(sender, **kwargs):
    logger.info("🔔 Checking schedule for send_reminders task...")

    try:
        if not Schedule.objects.filter(func='tracker.tasks.send_reminders').exists():
            Schedule.objects.create(
                name='Send Reminders',
                func='tracker.tasks.send_reminders',
                schedule_type=Schedule.MINUTES,
                minutes=30  # Run every 30 minutes — adjust as needed!
            )
            logger.info("✅ Scheduled send_reminders task successfully.")
        else:
            logger.info("⏭️ send_reminders task already scheduled — skipping.")
    except Exception as e:
        logger.error(f"❌ Failed to schedule send_reminders: {e}")
