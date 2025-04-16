from django.apps import AppConfig


class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    def ready(self):
        from background_task.models import Task
        from tracker.background_tasks.pushover import send_reminder_notifications

        # Check if task already exists, avoid duplicates
        if not Task.objects.filter(task_name="tracker.background_tasks.pushover.send_reminder_notifications").exists():
            send_reminder_notifications(repeat=3600)  # every hour

