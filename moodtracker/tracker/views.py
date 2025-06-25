import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import io
import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now, timedelta
from django.contrib.auth.decorators import login_required
from .models import Category, Question, Answer
from django.db.models import Prefetch
from django.http import HttpResponse
import pandas as pd
import matplotlib.dates as mdates


def home(request):  # Home page
    if request.user.is_authenticated:
        return redirect("answer_all")
    return render(request, "tracker/home.html")


@login_required
def question_list(request):  # List of questions
    """
    View to list all questions.
    """
    questions = Question.objects.all()
    return render(request, "tracker/question_list.html", {"questions": questions})


@login_required
def answer_question(request, question_id):  # answer a question
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        if question.question_type == Question.YES_NO:
            yes_no_answer = request.POST.get("yes_no") == "yes"
            Answer.objects.create(
                question=question,
                user=request.user,
                yes_no_answer=yes_no_answer,
                created_at=now(),
            )
        elif question.question_type == Question.SCALE:
            scale_answer = int(request.POST.get("scale"))
            Answer.objects.create(
                question=question,
                user=request.user,
                scale_answer=scale_answer,
                created_at=now(),
            )
        return redirect("question_list")

    return render(request, "tracker/answer_question.html", {"question": question})


@login_required
def answer_five_questions(request):
    # Fetch 5 random questions
    questions = Question.objects.order_by("?")[:5]
    scale_range = list(range(1, 8))  # Generate a list of numbers 1 to 10

    if request.method == "POST":
        for question in questions:
            if question.question_type == Question.YES_NO:
                yes_no_answer = request.POST.get(f"yes_no_{question.id}") == "yes"
                Answer.objects.create(
                    question=question,
                    user=request.user,
                    yes_no_answer=yes_no_answer,
                    created_at=now(),
                )
            elif question.question_type == Question.SCALE:
                scale_answer = request.POST.get(f"scale_{question.id}")
                if scale_answer:
                    Answer.objects.create(
                        question=question,
                        user=request.user,
                        scale_answer=int(scale_answer),
                        created_at=now(),
                    )
        return redirect("answer_five")  # Redirect to refresh with new questions

    context = {"questions": questions, "scale_range": scale_range}
    return render(request, "tracker/answer_five_questions.html", context)


@login_required
def answer_all_questions(request):
    # Fetch all questions ordered by their ID or other field if preferred
    questions = Question.objects.all().order_by("category__name")
    scale_range = list(range(1, 11))  # Updated scale range from 1 to 10

    if request.method == "POST":
        for question in questions:
            if question.question_type == Question.YES_NO:
                yes_no_answer = request.POST.get(f"yes_no_{question.id}") == "yes"
                Answer.objects.create(
                    question=question,
                    user=request.user,
                    yes_no_answer=yes_no_answer,
                    created_at=now(),
                )
            elif question.question_type == Question.SCALE:
                scale_answer = request.POST.get(f"scale_{question.id}")
                if scale_answer:
                    Answer.objects.create(
                        question=question,
                        user=request.user,
                        scale_answer=int(scale_answer),
                        created_at=now(),
                    )
        return redirect("answer_all")  # Redirect back to the same view

    context = {"questions": questions, "scale_range": scale_range}
    return render(request, "tracker/answer_questions.html", context)


@login_required
def answer_history(request):
    # Get the range from the query parameter or default to 10 days
    days = int(request.GET.get("days", 10))
    start_date = now() - timedelta(days=days)

    # Fetch answers within the specified range
    answers = Answer.objects.filter(
        user=request.user, created_at__gte=start_date
    ).order_by("-created_at")

    context = {
        "answers": answers,
        "days": days,
    }
    # Render different templates based on whether this is an HTMX request
    if request.htmx:
        return render(request, "tracker/partials/answer_history_list.html", context)
    return render(request, "tracker/answer_history.html", context)


@login_required
def question_chart(request, question_id):
    # Get the range from the query parameter or default to 10 days
    days = int(request.GET.get("days", 10))
    start_date = now() - timedelta(days=days)

    # Fetch the question and its answers
    question = Question.objects.get(id=question_id)
    category = question.category

    # Handle "View Category" request
    if request.GET.get("view_category") == "true":
        questions = category.questions.all()
        answers = Answer.objects.filter(
            question__in=questions, user=request.user, created_at__gte=start_date
        ).order_by("created_at")
        grouped_data = {
            q.text: [
                a.scale_answer if q.question_type == "SC" else int(a.yes_no_answer)
                for a in answers.filter(question=q).order_by("created_at")
            ]
            for q in questions
        }
    else:
        answers = Answer.objects.filter(
            question=question, user=request.user, created_at__gte=start_date
        ).order_by("created_at")
        grouped_data = {
            question.text: [
                (
                    a.scale_answer
                    if question.question_type == "SC"
                    else int(a.yes_no_answer)
                )
                for a in answers
            ]
        }

    # Generate the chart
    fig, ax = plt.subplots()
    for q_text, values in grouped_data.items():
        ax.plot(range(len(values)), values, label=q_text, marker="o")

    ax.set_title(
        f"Answers for: {category.name if request.GET.get('view_category') else question.text}"
    )
    ax.set_xlabel("Time")
    ax.set_ylabel("Answer")
    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    plt.xticks(rotation=45)

    # Convert chart to base64 string
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    chart_base64 = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()

    context = {
        "question": question,
        "chart": chart_base64,
        "days": days,
        "view_category": request.GET.get("view_category") == "true",
    }

    # Render appropriate template based on HTMX request
    if request.htmx:
        return render(request, "tracker/partials/chart.html", context)
    return render(request, "tracker/question_chart.html", context)


@login_required
def advanced_charts(request):
    days = int(request.GET.get("days", 30))
    mode = request.GET.get("mode", "multi")
    category_ids = request.GET.getlist("categories")
    start_date = now() - timedelta(days=days)

    all_categories = Category.objects.all()
    selected_categories = (
        Category.objects.filter(id__in=category_ids)
        if category_ids else all_categories
    )

    timeframes = [
        {"label": "1w", "days": 7},
        {"label": "1m", "days": 30},
        {"label": "3m", "days": 90},
        {"label": "6m", "days": 180},
        {"label": "1y", "days": 365},
    ]

    context = {
        "all_categories": all_categories,
        "selected_category_ids": list(map(str, category_ids)),
        "days": days,
        "mode": mode,
        "timeframes": timeframes,
    }

    if request.headers.get("Hx-Request"):
        return render(request, "tracker/partials/chart_filters_and_canvas.html", context)

    return render(request, "tracker/charts.html", context)




@login_required
def seaborn_chart_image(request):
    user = request.user
    days = int(request.GET.get("days", 30))
    mode = request.GET.get("mode", "multi")
    category_ids = request.GET.getlist("categories")
    start_date = now() - timedelta(days=days)

    selected_categories = (
        Category.objects.filter(id__in=category_ids)
        if category_ids else Category.objects.all()
    )

    questions = Question.objects.filter(category__in=selected_categories).prefetch_related(
        Prefetch(
            "answers",
            queryset=Answer.objects.filter(user=user, created_at__gte=start_date),
            to_attr="filtered_answers",
        )
    )

    # Setup plot
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid")

    for question in questions:
        dates = []
        values = []

        for answer in question.filtered_answers:
            if question.question_type == Question.SCALE and answer.scale_answer is not None:
                dates.append(answer.created_at)
                values.append(answer.scale_answer)
            elif question.question_type == Question.YES_NO and answer.yes_no_answer is not None:
                dates.append(answer.created_at)
                values.append(1 if answer.yes_no_answer else 0)

        if dates:
            sns.lineplot(x=dates, y=values, label=question.text)

    # Improve x-axis date formatting
    plt.gcf().autofmt_xdate()
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Answer", fontsize=12)

    # Improve legend layout
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save chart to PNG buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.read(), content_type="image/png")

@login_required
def chart_canvas_partial(request):
    # Same logic as above
    days = int(request.GET.get("days", 30))
    mode = request.GET.get("mode", "multi")
    category_ids = request.GET.getlist("categories")

    timeframes = [
        {"label": "1w", "days": 7},
        {"label": "1m", "days": 30},
        {"label": "3m", "days": 90},
        {"label": "6m", "days": 180},
        {"label": "1y", "days": 365},
    ]

    context = {
        "selected_category_ids": list(map(str, category_ids)),
        "days": days,
        "mode": mode,
        "timeframes": timeframes,
    }

    return render(request, "tracker/partials/chart_canvas_partial.html", context)



