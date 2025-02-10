from django.test import TestCase

from enrollments.models import Enrollment


class EnrollmentModelTests(TestCase):
    def test_defaults(self):
        obj = Enrollment.objects.create(ref="EN-100", amount_cents=500)
        self.assertEqual(obj.status, "open")
        self.assertEqual(str(obj), "EN-100")

    def test_ref_is_unique(self):
        Enrollment.objects.create(ref="EN-101", amount_cents=1)
        with self.assertRaises(Exception):
            Enrollment.objects.create(ref="EN-101", amount_cents=2)
