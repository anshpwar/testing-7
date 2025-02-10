from django.db import models

from courses.models import Course


class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(max_length=160)
    due_hour = models.PositiveIntegerField(default=0, help_text="hours since term start")

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    prompt = models.CharField(max_length=240)
    answer_key = models.CharField(max_length=120)
    points = models.PositiveSmallIntegerField(default=1)


class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    student = models.CharField(max_length=40)
    submitted_hour = models.PositiveIntegerField(default=0)
    raw_points = models.PositiveIntegerField(default=0)
    final_percent = models.PositiveSmallIntegerField(default=0)
