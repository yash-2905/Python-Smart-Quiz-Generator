from django.contrib import admin
from .models import Question, QuizResult


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "question_text", "correct_answer")
    search_fields = ("topic", "question_text")


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("id", "topic", "score", "total", "percentage", "created_at")