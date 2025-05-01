from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("questions/", views.question_list, name="question_list"),  # List of questions
    path(
        "questions/<int:question_id>/answer/",
        views.answer_question,
        name="answer_question",
    ),  # Answer a question
    path("answer/", views.answer_question, name="answer_question"),  # Answer question
    path("answer-history/", views.answer_history, name="answer_history"),
    path(
        "question-chart/<int:question_id>/", views.question_chart, name="question_chart"
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="tracker/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("answer_all/", views.answer_all_questions, name="answer_all"),
]
