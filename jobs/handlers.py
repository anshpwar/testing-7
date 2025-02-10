"""Built-in handlers: deadline reminders and grade recomputation."""
from courses.models import Course
from grading import services as grading
from lmskit import rules

from .queue import enqueue, handler

SENT = []


@handler("send_reminder")
def send_reminder(payload):
    SENT.append((payload["student"], payload["quiz"]))


@handler("recompute_grades")
def recompute_grades(payload):
    grading.record_grades(Course.objects.get(code=payload["course"]))


def schedule_reminder(student, quiz_title, due_hour, now_hour):
    lead = rules.reminder_lead_hours(max(0, (due_hour - now_hour) // 24))
    run_after = max(0, (due_hour - lead) * 3600)
    return enqueue("send_reminder", {"student": student, "quiz": quiz_title}, priority=1, run_after=run_after)
