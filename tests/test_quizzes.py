from django.test import TestCase

from lmskit import rules
from quizzes import services

from .factories import make_course, make_quiz


class ScoringTests(TestCase):
    def setUp(self):
        self.course = make_course(credits=3)
        self.quiz, self.qs = make_quiz(self.course, due_hour=100)

    def test_raw_score_is_case_and_space_insensitive(self):
        answers = {self.qs[0].id: " A ", self.qs[1].id: "B", self.qs[2].id: "x"}
        self.assertEqual(services.raw_score(self.quiz, answers), 2)

    def test_on_time_has_no_penalty(self):
        self.assertEqual(services.late_penalty_bp(self.quiz, 100), 0)
        self.assertEqual(services.late_penalty_bp(self.quiz, 90), 0)

    def test_late_penalty_follows_policy_and_is_capped(self):
        self.assertEqual(services.late_penalty_bp(self.quiz, 130), min(10000, rules.late_penalty_bp(30)))
        self.assertLessEqual(services.late_penalty_bp(self.quiz, 100000), 10000)

    def test_percent_after_penalty(self):
        self.assertEqual(services.percent_after_penalty(4, 4, 0), 100)
        self.assertEqual(services.percent_after_penalty(2, 4, 1000), 45)
        self.assertEqual(services.percent_after_penalty(0, 0, 0), 0)

    def test_submit_records_attempt(self):
        answers = {q.id: k for q, k in zip(self.qs, "abcd")}
        attempt = services.submit(self.quiz, "ana", answers, 100)
        self.assertEqual((attempt.raw_points, attempt.final_percent), (4, 100))

    def test_attempt_limit_follows_policy(self):
        limit = rules.attempts_allowed(3)
        for _ in range(limit):
            services.submit(self.quiz, "ben", {}, 100)
        with self.assertRaises(services.AttemptsExhausted):
            services.submit(self.quiz, "ben", {}, 100)

    def test_time_limit_follows_policy(self):
        self.assertEqual(services.time_limit_minutes(self.quiz), rules.quiz_time_limit_min(4))
