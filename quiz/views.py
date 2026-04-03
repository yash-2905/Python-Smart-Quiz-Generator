import random
from django.shortcuts import render
from .models import Question

def home(request):
    return render(request, 'home.html')

def quiz(request):
    if request.method == "POST":
        topic = request.POST.get("topic")
        num_questions = request.POST.get("num_questions")

        if not topic or not num_questions:
            return render(request, "home.html", {"error": "Please fill all fields"})

        try:
            num_questions = int(num_questions)
            if num_questions <= 0:
                raise ValueError
        except:
            return render(request, "home.html", {"error": "Enter a valid positive number"})

        questions = Question.objects.filter(topic__icontains=topic)

        if not questions.exists():
            return render(request, "home.html", {"error": "No questions found for this topic"})

        # Safe Random Selection
        all_questions = list(questions)
        selected_questions = random.sample(all_questions, min(num_questions, len(all_questions)))

        return render(request, "quiz.html", {
            "topic": topic,
            "questions": selected_questions
        })
    
    return render(request, "home.html")

def result(request):
    if request.method == "POST":
        score = 0
        # Sirf question keys nikalna (q1, q2 etc)
        question_keys = [key for key in request.POST if key.startswith("q") and not key.endswith("_correct")]
        total = len(question_keys)

        for key in question_keys:
            user_answer = request.POST.get(key)
            q_id = key.replace("q", "")
            
            try:
                # DATABASE se answer check karna (Security Fix)
                question_obj = Question.objects.get(id=q_id)
                if user_answer and question_obj.correct_answer:
                    if user_answer.strip().upper() == question_obj.correct_answer.strip().upper():
                        score += 1
            except Question.DoesNotExist:
                continue

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