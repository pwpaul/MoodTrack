from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Home page (already set up previously)
    path("questions/", views.question_list, name="question_list"),  # List of questions
    path(
        "questions/<int:question_id>/answer/",
        views.answer_question,
        name="answer_question",
    ),  # Answer a question
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="tracker/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
