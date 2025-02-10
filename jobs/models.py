from django.db import models


class Job(models.Model):
    STATUSES = [("queued", "Queued"), ("done", "Done"), ("dead", "Dead")]

    kind = models.CharField(max_length=40)
    payload = models.TextField(default="{}")
    priority = models.PositiveSmallIntegerField(default=2)
    status = models.CharField(max_length=8, choices=STATUSES, default="queued")
    attempts = models.PositiveSmallIntegerField(default=0)
    run_after = models.PositiveIntegerField(default=0)
    last_error = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        ordering = ["run_after", "priority", "id"]
