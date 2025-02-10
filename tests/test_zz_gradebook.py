from django.test import TestCase

from grading import services
from quizzes.services import submit

from .factories import make_course, make_quiz


class GradebookViewTests(TestCase):
    def setUp(self):
        self.course = make_course()
        quiz, qs = make_quiz(self.course)
        for student, right in (("ana", 4), ("ben", 2)):
            submit(quiz, student, {q.id: q.answer_key for q in qs[:right]}, 10)
        services.record_grades(self.course)

    def test_gradebook_lists_students_best_first(self):
        resp = self.client.get("/gradebook/CS101/")
        body = resp.content.decode()
        self.assertLess(body.index("ana"), body.index("ben"))
        self.assertContains(resp, "100%")

    def test_unknown_course(self):
        self.assertEqual(self.client.get("/gradebook/NOPE/").status_code, 404)

    def test_pagination_context(self):
        resp = self.client.get("/gradebook/CS101/?page=1")
        self.assertEqual(resp.context["page"], 1)
        self.assertEqual(len(resp.context["rows"]), 2)
