from django.db.models.signals import post_migrate
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)  # 📜 standard logging

@receiver(post_migrate)
def schedule_send_reminders(sender, **kwargs):
    logger.info("🔔 Scheduling send_reminders from signals.py...")
    from background_task.models import Task  # ✅ Move imports *here*, inside function
    from tracker.tasks import send_reminders  # ✅ Import here too

    if not Task.objects.filter(task_name='tracker.tasks.send_reminders').exists():
        send_reminders(schedule=5, repeat=3600)
