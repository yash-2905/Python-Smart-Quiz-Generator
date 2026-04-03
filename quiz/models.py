from django.db import models

class Question(models.Model):
    topic = models.CharField(max_length=100)
    question_text = models.TextField()

    option_1 = models.CharField(max_length=255)
    option_2 = models.CharField(max_length=255)
    option_3 = models.CharField(max_length=255)
    option_4 = models.CharField(max_length=255)

    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text


class QuizResult(models.Model):
    topic = models.CharField(max_length=100)
    score = models.IntegerField()
    total = models.IntegerField()
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} - {self.score}/{self.total}"