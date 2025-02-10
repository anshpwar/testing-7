import json

from django.test import TestCase

from .factories import make_course


class CourseViewTests(TestCase):
    def setUp(self):
        make_course("CS101")
        make_course("MA201", credits=4, lessons=((1, "Limits", 40),))

    def test_list_page(self):
        resp = self.client.get("/courses/")
        self.assertContains(resp, "CS101")
        self.assertContains(resp, "4 credits")

    def test_detail_page_shows_lessons_and_total(self):
        resp = self.client.get("/courses/CS101/")
        self.assertContains(resp, "3 lessons, 100 minutes in total.")
        self.assertContains(resp, "Loops (35 min)")

    def test_unknown_course_404(self):
        self.assertEqual(self.client.get("/courses/NOPE/").status_code, 404)

    def test_json_listing(self):
        data = json.loads(self.client.get("/courses/json/").content)
        self.assertEqual([c["code"] for c in data["courses"]], ["CS101", "MA201"])
