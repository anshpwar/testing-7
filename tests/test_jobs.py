from django.test import TestCase

from jobs import handlers, queue
from jobs.models import Job
from lmskit import rules


class QueueTests(TestCase):
    def setUp(self):
        self.calls = []

        @queue.handler("test_ok")
        def ok(payload):
            self.calls.append(payload)

        @queue.handler("test_boom")
        def boom(payload):
            raise RuntimeError("nope")

    def test_success_marks_done(self):
        job = queue.enqueue("test_ok", {"n": 1})
        queue.run_due(0)
        job.refresh_from_db()
        self.assertEqual((job.status, job.attempts), ("done", 1))
        self.assertEqual(self.calls, [{"n": 1}])

    def test_future_jobs_wait(self):
        queue.enqueue("test_ok", run_after=500)
        self.assertEqual(queue.run_due(499), [])
        self.assertEqual(len(queue.run_due(500)), 1)

    def test_failure_schedules_backoff_from_policy(self):
        job = queue.enqueue("test_boom", priority=1)
        queue.run_due(1000)
        job.refresh_from_db()
        if rules.max_job_attempts(1) > 1:
            self.assertEqual((job.status, job.run_after), ("queued", 1000 + rules.retry_backoff_s(1)))
        self.assertIn("RuntimeError", job.last_error)

    def test_job_dies_after_policy_attempts(self):
        job = queue.enqueue("test_boom", priority=3)
        now = 0
        for _ in range(rules.max_job_attempts(3) + 1):
            job.refresh_from_db()
            if job.status == "dead":
                break
            now = max(now, job.run_after)
            queue.run_due(now)
        job.refresh_from_db()
        self.assertEqual(job.status, "dead")
        self.assertEqual(job.attempts, rules.max_job_attempts(3))

    def test_unknown_kind_is_recorded_not_raised(self):
        job = queue.enqueue("mystery")
        queue.run_due(0)
        job.refresh_from_db()
        self.assertIn("LookupError", job.last_error)

    def test_reminder_scheduling_uses_policy(self):
        job = handlers.schedule_reminder("ana", "Quiz 1", due_hour=240, now_hour=0)
        lead = rules.reminder_lead_hours(10)
        self.assertEqual(job.run_after, max(0, (240 - lead) * 3600))
        self.assertEqual(Job.objects.get(pk=job.pk).priority, 1)
