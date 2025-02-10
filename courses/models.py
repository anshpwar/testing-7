from django.db import models


class Course(models.Model):
    code = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=160)
    credits = models.PositiveSmallIntegerField(default=3)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} {self.title}"

    def total_minutes(self):
        return sum(self.lessons.values_list("minutes", flat=True))


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=160)
    minutes = models.PositiveSmallIntegerField(default=20)

    class Meta:
        ordering = ["course", "order"]
        unique_together = [("course", "order")]

    def __str__(self):
        return f"{self.course.code}/{self.order} {self.title}"
