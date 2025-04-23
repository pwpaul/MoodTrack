from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    goal_statement = models.TextField(null=True, blank=True)
    pushover_user_key = models.CharField(max_length=30, blank=True, null=True)
    pushover_device_name = models.CharField(max_length=30, blank=True, null=True)
    pushover_app_token = models.CharField(max_length=30, blank=True, null=True)
    reminder_interval_hours = models.PositiveIntegerField(default=12)  # e.g. 12 hours
    last_reminder_sent = models.DateTimeField(null=True, blank=True) #for reminder tracking


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    YES_NO = "YN"
    SCALE = "SC"

    QUESTION_TYPES = [
        (YES_NO, "Yes/No"),
        (SCALE, "Scale (1-10)"),
    ]

    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="questions"
    )
    text = models.CharField(max_length=255)
    question_type = models.CharField(
        max_length=2, choices=QUESTION_TYPES, default=YES_NO
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    yes_no_answer = models.BooleanField(null=True, blank=True)  # For Yes/No questions
    scale_answer = models.IntegerField(
        null=True, blank=True
    )  # For Scale questions (1-10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user} on {self.created_at}"
