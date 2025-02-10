from django.core.management.base import BaseCommand

from jobs import handlers  # noqa: F401  (registers the built-in handlers)
from jobs.queue import run_due


class Command(BaseCommand):
    help = "Run every queued job that is due at --now (seconds since epoch)."

    def add_arguments(self, parser):
        parser.add_argument("--now", type=int, required=True)

    def handle(self, *args, **opts):
        ran = run_due(opts["now"])
        done = sum(1 for j in ran if j.status == "done")
        self.stdout.write(f"ran {len(ran)} jobs, {done} done, {len(ran) - done} not done")
