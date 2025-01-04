from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from django.utils.timezone import now

@login_required
def home(request):
    return render(request, "tracker/home.html")


@login_required
def question_list(request):
    """
    View to list all questions.
    """
    questions = Question.objects.all()
    return render(request, "tracker/question_list.html", {"questions": questions})


@login_required
def answer_question(request, question_id):
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
