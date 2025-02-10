"""A small database-backed job queue with policy-driven retries. Time is passed in (seconds), never read."""
import json

from lmskit import rules

from .models import Job

HANDLERS = {}


def handler(kind):
    def deco(fn):
        HANDLERS[kind] = fn
        return fn
    return deco


def enqueue(kind, payload=None, priority=2, run_after=0):
    return Job.objects.create(kind=kind, payload=json.dumps(payload or {}, sort_keys=True), priority=priority, run_after=run_after)


def due(now):
    return Job.objects.filter(status="queued", run_after__lte=now)


def run_one(job, now):
    fn = HANDLERS.get(job.kind)
    job.attempts += 1
    try:
        if fn is None:
            raise LookupError(f"no handler for {job.kind}")
        fn(json.loads(job.payload))
        job.status = "done"
        job.last_error = ""
    except Exception as exc:  # job handlers are arbitrary; the queue records the failure
        job.last_error = f"{type(exc).__name__}: {exc}"[:200]
        if job.attempts >= rules.max_job_attempts(job.priority):
            job.status = "dead"
        else:
            job.run_after = now + rules.retry_backoff_s(job.attempts)
    job.save()
    return job


def run_due(now):
    ran = []
    for job in list(due(now)):
        ran.append(run_one(job, now))
    return ran
