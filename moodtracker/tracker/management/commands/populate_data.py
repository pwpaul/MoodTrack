from django.core.management.base import BaseCommand
from tracker.models import Category, Question, Answer, CustomUser
from django.utils.timezone import now
from random import randint, choice


class Command(BaseCommand):
    help = "Populate the database with sample categories, questions, and answers"

    def handle(self, *args, **kwargs):

        # delete current data
        Answer.objects.all().delete()
        Question.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write("Existing data cleared.")

        # Create or get a superuser for testing
        admin_user, created = CustomUser.objects.get_or_create(
            username="paul", defaults={"email": "paul.beauvais@gmail.com"}
        )
        if created:
            admin_user.set_password("Pjb7412J")
            admin_user.save()
            self.stdout.write("Superuser 'paul' created.")
        else:
            self.stdout.write("Superuser 'paul' already exists.")

            # Create or get a superuser for testing
        admin_user, created = CustomUser.objects.get_or_create(
            username="ashley", defaults={"email": "computerwiz102@gmail.com"}
        )
        if created:
            admin_user.set_password("dontjizzeverywhere")
            admin_user.save()
            self.stdout.write("Superuser 'ashley' created.")
        else:
            self.stdout.write("Superuser 'ashley' already exists.")

        # Add categories
        categories = [
            "Mental Health",
            "Physical Health",
            "Productivity",
            "Relationships",
            "Hobbies",
        ]
        category_objects = []

        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(f"Created category: {category_name}")
            else:
                self.stdout.write(f"Category already exists: {category_name}")
            category_objects.append(category)

        # Add questions with appropriate types
        questions = {
            "Mental Health": [
                ("How was your mood today (solo)?", Question.SCALE),
                ("How was your mood today (social)?", Question.SCALE),
                ("Have I cried or wanted to cry?", Question.YES_NO),
                ("Did I feel 'out of control'?", Question.YES_NO),
            ],
            "Physical Health": [
                ("Did you exercise today?", Question.YES_NO),
                ("Rate your sleep quality last night?", Question.SCALE),
                ("Did you eat well today?", Question.YES_NO),
                (
                    "Feeling on Appearance, scale 1-7, 1=Unattractive/Fat/Weak 7=Attractive/Fit/Strong",
                    Question.SCALE,
                ),
            ],
            "Relationships": [
                ("Did you connect with friends or family today?", Question.YES_NO),
            ],
        }

        question_objects = []
        for category_name, question_data in questions.items():
            category = Category.objects.get(name=category_name)
            for text, question_type in question_data:
                question, created = Question.objects.get_or_create(
                    category=category, text=text, question_type=question_type
                )
                if created:
                    self.stdout.write(f"Created question: {text}")
                else:
                    self.stdout.write(f"Question already exists: {text}")
                question_objects.append(question)

        # Add sample answers for the admin user
        for question in question_objects:
            if not Answer.objects.filter(question=question, user=admin_user).exists():
                if question.question_type == Question.YES_NO:
                    yes_no_answer = choice([True, False])
                    Answer.objects.create(
                        question=question,
                        user=admin_user,
                        yes_no_answer=yes_no_answer,
                        created_at=now(),
                    )
                    self.stdout.write(
                        f"Added Yes/No answer for question: {question.text}"
                    )
                elif question.question_type == Question.SCALE:
                    scale_answer = randint(1, 10)
                    Answer.objects.create(
                        question=question,
                        user=admin_user,
                        scale_answer=scale_answer,
                        created_at=now(),
                    )
                    self.stdout.write(
                        f"Added Scale answer for question: {question.text}"
                    )
            else:
                self.stdout.write(
                    f"Answer already exists for question: {question.text}"
                )

        self.stdout.write("Data population complete!")
