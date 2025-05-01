from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Category, Question, Answer
from django.utils.translation import gettext_lazy as _
from django.contrib import admin



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Extend the "Personal info" section
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "pushover_device_name",
                    "pushover_user_key",
                    "pushover_app_token",
                    "reminder_interval_hours",
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "pushover_user_key",
                    "pushover_device_name",
                    "pushover_app_token",
                    "reminder_interval_hours",
                ),
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "pushover_user_key",
        "pushover_device_name",
        "pushover_app_token",
        "reminder_interval_hours",
        "is_staff",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "category", "question_type")
    list_filter = ("category", "question_type")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question", "user", "created_at")
