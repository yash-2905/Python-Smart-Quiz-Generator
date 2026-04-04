from django.contrib.auth.models import User
from django.http import HttpResponse
import random
from django.shortcuts import render
from .models import Question


def home(request):
    return render(request, "home.html")


def quiz(request):
    if request.method == "POST":
        topic = request.POST.get("topic")
        num_questions = request.POST.get("num_questions")

        # ✅ Validation fix
        if not topic or num_questions is None or num_questions == "":
            return render(request, "home.html", {"error": "Please fill all fields"})

        try:
            num_questions = int(num_questions)
            if num_questions <= 0:
                raise ValueError
        except:
            return render(request, "home.html", {"error": "Enter a valid number"})

        # ✅ DB se questions fetch
        questions = Question.objects.filter(topic__icontains=topic)

        if not questions:
            return render(request, "home.html", {"error": "No question found for this topic"})

        all_questions = list(questions)

        selected_questions = random.sample(
            all_questions,
            min(num_questions, len(all_questions))
        )

        return render(request, "quiz.html", {
            "topic": topic,
            "questions": selected_questions
        })

    return render(request, "home.html")


def result(request):
    if request.method == "POST":
        score = 0

        question_keys = [
            key for key in request.POST 
            if key.startswith("q") and not key.endswith("_correct")
        ]

        total = len(question_keys)

        for key in question_keys:
            user_answer = request.POST.get(key)
            correct_answer = request.POST.get(f"{key}_correct")

            if user_answer and correct_answer:
                if user_answer.strip().upper() == correct_answer.strip().upper():
                    score += 1

        wrong_answers = total - score
        percentage = (score / total) * 100 if total > 0 else 0

        if percentage >= 80:
            message = "Excellent! Very good performance"
        elif percentage >= 50:
            message = "Good job! Keep practicing"
        else:
            message = "Needs improvement. Practice more"

        return render(request, "result.html", {
            "score": score,
            "total": total,
            "wrong_answers": wrong_answers,
            "percentage": int(percentage),
            "message": message
        })
def create_admin(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='admin123'
        )
        return HttpResponse("Superuser created")
    else:
        return HttpResponse("Already exists")