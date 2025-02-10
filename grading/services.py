"""Final grades from quiz attempts. Letter bands come from the policy tables."""
from lmskit import rules
from quizzes.models import Attempt

from .models import Grade


def best_per_quiz(course, student):
    best = {}
    for a in Attempt.objects.filter(quiz__course=course, student=student):
        best[a.quiz_id] = max(best.get(a.quiz_id, 0), a.final_percent)
    return best


def final_percent(course, student):
    best = best_per_quiz(course, student)
    return round(sum(best.values()) / len(best)) if best else 0


def letter_for(percent, class_size):
    a_floor = rules.grade_a_floor_pct(class_size)
    if percent >= a_floor:
        return "A"
    for letter, floor in (("B", a_floor - 10), ("C", a_floor - 20), ("D", a_floor - 30)):
        if percent >= floor:
            return letter
    return "F"


def record_grades(course):
    students = sorted(set(Attempt.objects.filter(quiz__course=course).values_list("student", flat=True)))
    mark = rules.pass_mark_pct(course.credits)
    for s in students:
        pct = final_percent(course, s)
        Grade.objects.update_or_create(course=course, student=s, defaults={
            "percent": pct, "letter": letter_for(pct, len(students)), "passed": pct >= mark})
    return len(students)


def page_size(student_count):
    return rules.gradebook_page_size(student_count)
