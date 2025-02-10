import io

from django.core.management import call_command
from django.test import TestCase

from courses.models import Course
from grading.models import Grade
from jobs import handlers, queue
from quizzes.services import submit

from .factories import make_course, make_quiz


class RunJobsCommandTests(TestCase):
    def test_command_runs_due_jobs_and_recomputes_grades(self):
        course = make_course()
        quiz, qs = make_quiz(course)
        submit(quiz, "ana", {q.id: q.answer_key for q in qs}, 10)
        queue.enqueue("recompute_grades", {"course": "CS101"})
        queue.enqueue("send_reminder", {"student": "ana", "quiz": "q"}, run_after=10**6)
        out = io.StringIO()
        call_command("runjobs", now=5, stdout=out)
        self.assertIn("ran 1 jobs, 1 done", out.getvalue())
        self.assertEqual(Grade.objects.get(student="ana").percent, 100)
        self.assertEqual(handlers.SENT, [])
