from django.test import TestCase

from courses import services
from lmskit import rules

from .factories import make_course


class CourseModelTests(TestCase):
    def test_total_minutes_and_ordering(self):
        course = make_course()
        self.assertEqual(course.total_minutes(), 100)
        self.assertEqual([l.order for l in course.lessons.all()], [1, 2, 3])

    def test_lesson_order_is_unique_per_course(self):
        course = make_course()
        with self.assertRaises(Exception):
            course.lessons.create(order=1, title="dup", minutes=1)

    def test_next_lesson(self):
        course = make_course()
        self.assertEqual(services.next_lesson(course, []).order, 1)
        self.assertEqual(services.next_lesson(course, [1, 2]).order, 3)
        self.assertIsNone(services.next_lesson(course, [1, 2, 3]))

    def test_policy_lookups(self):
        course = make_course(credits=6)
        self.assertEqual(services.attempts_for(course), rules.attempts_allowed(6))
        self.assertEqual(services.pass_mark_for(course), rules.pass_mark_pct(6))
        self.assertEqual(services.video_cache_hours(course.lessons.first()), rules.video_cache_hours(20))
