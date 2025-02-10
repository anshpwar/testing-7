from django.test import TestCase

from grading import services
from grading.models import Grade
from lmskit import rules
from quizzes.services import submit

from .factories import make_course, make_quiz


class GradingTests(TestCase):
    def setUp(self):
        self.course = make_course(credits=3)
        self.quiz1, self.q1 = make_quiz(self.course, due_hour=100)
        self.quiz2, self.q2 = make_quiz(self.course, due_hour=200, answers=("x", "y"))

    def attempt(self, quiz, qs, student, right, hour=50):
        answers = {q.id: key for q, key in zip(qs, [q.answer_key for q in qs][:right])}
        return submit(quiz, student, answers, hour)

    def test_final_percent_uses_best_attempt_per_quiz(self):
        self.attempt(self.quiz1, self.q1, "ana", 2)
        self.attempt(self.quiz1, self.q1, "ana", 4)
        self.attempt(self.quiz2, self.q2, "ana", 1)
        self.assertEqual(services.final_percent(self.course, "ana"), round((100 + 50) / 2))

    def test_no_attempts_is_zero(self):
        self.assertEqual(services.final_percent(self.course, "nobody"), 0)

    def test_letter_bands_are_relative_to_the_a_floor(self):
        floor = rules.grade_a_floor_pct(30)
        self.assertEqual(services.letter_for(floor, 30), "A")
        self.assertEqual(services.letter_for(floor - 10, 30), "B")
        self.assertEqual(services.letter_for(floor - 20, 30), "C")
        self.assertEqual(services.letter_for(floor - 30, 30), "D")
        self.assertEqual(services.letter_for(floor - 31, 30), "F")

    def test_record_grades_creates_and_updates(self):
        self.attempt(self.quiz1, self.q1, "ana", 4)
        self.attempt(self.quiz1, self.q1, "ben", 1)
        self.assertEqual(services.record_grades(self.course), 2)
        ana = Grade.objects.get(student="ana")
        self.assertEqual(ana.percent, 100)
        self.assertEqual(ana.passed, 100 >= rules.pass_mark_pct(3))
        self.assertEqual(services.record_grades(self.course), 2)
        self.assertEqual(Grade.objects.count(), 2)

    def test_page_size_follows_policy(self):
        self.assertEqual(services.page_size(100), rules.gradebook_page_size(100))
