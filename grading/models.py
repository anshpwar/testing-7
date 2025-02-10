from django.db import models

from courses.models import Course


class Grade(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="grades")
    student = models.CharField(max_length=40)
    percent = models.PositiveSmallIntegerField()
    letter = models.CharField(max_length=2)
    passed = models.BooleanField(default=False)

    class Meta:
        unique_together = [("course", "student")]
        ordering = ["course", "-percent", "student"]
