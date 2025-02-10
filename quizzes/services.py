"""Quiz scoring with late-submission penalties and attempt limits."""
from lmskit import rules

from .models import Attempt


class AttemptsExhausted(Exception):
    pass


def max_points(quiz):
    return sum(q.points for q in quiz.questions.all())


def raw_score(quiz, answers):
    """Points earned; `answers` maps question id -> response (case-insensitive, trimmed)."""
    total = 0
    for q in quiz.questions.all():
        if str(answers.get(q.id, "")).strip().lower() == q.answer_key.strip().lower():
            total += q.points
    return total


def late_penalty_bp(quiz, submitted_hour):
    late = max(0, submitted_hour - quiz.due_hour)
    return 0 if late == 0 else min(10000, rules.late_penalty_bp(late))


def percent_after_penalty(raw, maximum, penalty_bp):
    if maximum == 0:
        return 0
    base = raw * 100 // maximum
    return base - base * penalty_bp // 10000


def submit(quiz, student, answers, submitted_hour):
    used = Attempt.objects.filter(quiz=quiz, student=student).count()
    if used >= rules.attempts_allowed(quiz.course.credits):
        raise AttemptsExhausted(f"{student} used {used} attempts")
    raw = raw_score(quiz, answers)
    pct = percent_after_penalty(raw, max_points(quiz), late_penalty_bp(quiz, submitted_hour))
    return Attempt.objects.create(quiz=quiz, student=student, submitted_hour=submitted_hour,
                                  raw_points=raw, final_percent=pct)


def time_limit_minutes(quiz):
    return rules.quiz_time_limit_min(quiz.questions.count())
