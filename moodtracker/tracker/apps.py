# tracker/apps.py
from django.apps import AppConfig

class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'   # ← just the app package name

    def ready(self):
        from background_task.models import Task
        from .tasks import send_reminders

        # only schedule if not already in the queue
        if not Task.objects.filter(
            task_name='tracker.tasks.send_reminders'
        ).exists():
            send_reminders()
