"""Course scheduling helpers backed by the lmskit policy tables."""
from lmskit import rules


def video_cache_hours(lesson):
    return rules.video_cache_hours(lesson.minutes)


def attempts_for(course):
    return rules.attempts_allowed(course.credits)


def pass_mark_for(course):
    return rules.pass_mark_pct(course.credits)


def next_lesson(course, completed_orders):
    """First lesson the student has not completed, or None."""
    done = set(completed_orders)
    for lesson in course.lessons.all():
        if lesson.order not in done:
            return lesson
    return None
