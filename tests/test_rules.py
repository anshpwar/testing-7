import unittest

from lmskit import rules


class RuleTests(unittest.TestCase):
    def test_certificate_hours_required(self):
        self.assertEqual(rules.certificate_hours_required(0), 10)
        self.assertEqual(rules.certificate_hours_required(1), 10)
        self.assertEqual(rules.certificate_hours_required(2), 30)
        self.assertEqual(rules.certificate_hours_required(3), 30)
        self.assertEqual(rules.certificate_hours_required(4), 60)
        self.assertEqual(rules.certificate_hours_required(6), 60)
        self.assertEqual(rules.certificate_hours_required(7), 120)

    def test_plagiarism_similarity_limit_pct(self):
        self.assertEqual(rules.plagiarism_similarity_limit_pct(0), 40)
        self.assertEqual(rules.plagiarism_similarity_limit_pct(1), 40)
        self.assertEqual(rules.plagiarism_similarity_limit_pct(500), 40)
        self.assertEqual(rules.plagiarism_similarity_limit_pct(501), 30)
        self.assertEqual(rules.plagiarism_similarity_limit_pct(2000), 30)
        self.assertEqual(rules.plagiarism_similarity_limit_pct(2001), 20)
        self.assertEqual(rules.plagiarism_similarity_limit_pct(10000), 20)
        self.assertEqual(rules.plagiarism_similarity_limit_pct(10001), 15)

    def test_late_penalty_bp(self):
        self.assertEqual(rules.late_penalty_bp(0), 500)
        self.assertEqual(rules.late_penalty_bp(1), 500)
        self.assertEqual(rules.late_penalty_bp(24), 500)
        self.assertEqual(rules.late_penalty_bp(25), 1500)
        self.assertEqual(rules.late_penalty_bp(72), 1500)
        self.assertEqual(rules.late_penalty_bp(73), 3000)
        self.assertEqual(rules.late_penalty_bp(168), 3000)
        self.assertEqual(rules.late_penalty_bp(169), 5000)

    def test_retry_backoff_s(self):
        self.assertEqual(rules.retry_backoff_s(0), 27)
        self.assertEqual(rules.retry_backoff_s(1), 27)
        self.assertEqual(rules.retry_backoff_s(2), 263)
        self.assertEqual(rules.retry_backoff_s(3), 263)
        self.assertEqual(rules.retry_backoff_s(4), 1575)
        self.assertEqual(rules.retry_backoff_s(6), 1575)
        self.assertEqual(rules.retry_backoff_s(7), 6300)

    def test_max_job_attempts(self):
        self.assertEqual(rules.max_job_attempts(0), 10)
        self.assertEqual(rules.max_job_attempts(1), 10)
        self.assertEqual(rules.max_job_attempts(2), 5)
        self.assertEqual(rules.max_job_attempts(3), 3)
        self.assertEqual(rules.max_job_attempts(4), 2)

    def test_reminder_lead_hours(self):
        self.assertEqual(rules.reminder_lead_hours(0), 2)
        self.assertEqual(rules.reminder_lead_hours(1), 2)
        self.assertEqual(rules.reminder_lead_hours(2), 12)
        self.assertEqual(rules.reminder_lead_hours(3), 12)
        self.assertEqual(rules.reminder_lead_hours(4), 24)
        self.assertEqual(rules.reminder_lead_hours(7), 24)
        self.assertEqual(rules.reminder_lead_hours(8), 48)

    def test_quiz_time_limit_min(self):
        self.assertEqual(rules.quiz_time_limit_min(0), 15)
        self.assertEqual(rules.quiz_time_limit_min(1), 15)
        self.assertEqual(rules.quiz_time_limit_min(10), 15)
        self.assertEqual(rules.quiz_time_limit_min(11), 45)
        self.assertEqual(rules.quiz_time_limit_min(30), 45)
        self.assertEqual(rules.quiz_time_limit_min(31), 90)
        self.assertEqual(rules.quiz_time_limit_min(60), 90)
        self.assertEqual(rules.quiz_time_limit_min(61), 150)

    def test_attempts_allowed(self):
        self.assertEqual(rules.attempts_allowed(0), 5)
        self.assertEqual(rules.attempts_allowed(1), 5)
        self.assertEqual(rules.attempts_allowed(2), 3)
        self.assertEqual(rules.attempts_allowed(3), 3)
        self.assertEqual(rules.attempts_allowed(4), 2)
        self.assertEqual(rules.attempts_allowed(6), 2)
        self.assertEqual(rules.attempts_allowed(7), 2)

    def test_grade_a_floor_pct(self):
        self.assertEqual(rules.grade_a_floor_pct(0), 90)
        self.assertEqual(rules.grade_a_floor_pct(1), 90)
        self.assertEqual(rules.grade_a_floor_pct(10), 90)
        self.assertEqual(rules.grade_a_floor_pct(11), 92)
        self.assertEqual(rules.grade_a_floor_pct(50), 92)
        self.assertEqual(rules.grade_a_floor_pct(51), 94)
        self.assertEqual(rules.grade_a_floor_pct(200), 94)
        self.assertEqual(rules.grade_a_floor_pct(201), 95)

    def test_pass_mark_pct(self):
        self.assertEqual(rules.pass_mark_pct(0), 50)
        self.assertEqual(rules.pass_mark_pct(1), 50)
        self.assertEqual(rules.pass_mark_pct(2), 55)
        self.assertEqual(rules.pass_mark_pct(3), 55)
        self.assertEqual(rules.pass_mark_pct(4), 60)
        self.assertEqual(rules.pass_mark_pct(6), 60)
        self.assertEqual(rules.pass_mark_pct(7), 65)

    def test_extension_days(self):
        self.assertEqual(rules.extension_days(0), 2)
        self.assertEqual(rules.extension_days(1), 2)
        self.assertEqual(rules.extension_days(2), 5)
        self.assertEqual(rules.extension_days(3), 10)
        self.assertEqual(rules.extension_days(4), 14)

    def test_forum_post_rate_limit(self):
        self.assertEqual(rules.forum_post_rate_limit(0), 3)
        self.assertEqual(rules.forum_post_rate_limit(1), 3)
        self.assertEqual(rules.forum_post_rate_limit(2), 10)
        self.assertEqual(rules.forum_post_rate_limit(7), 10)
        self.assertEqual(rules.forum_post_rate_limit(8), 30)
        self.assertEqual(rules.forum_post_rate_limit(30), 30)
        self.assertEqual(rules.forum_post_rate_limit(31), 100)

    def test_video_cache_hours(self):
        self.assertEqual(rules.video_cache_hours(0), 24)
        self.assertEqual(rules.video_cache_hours(1), 24)
        self.assertEqual(rules.video_cache_hours(5), 24)
        self.assertEqual(rules.video_cache_hours(6), 72)
        self.assertEqual(rules.video_cache_hours(30), 72)
        self.assertEqual(rules.video_cache_hours(31), 168)
        self.assertEqual(rules.video_cache_hours(120), 168)
        self.assertEqual(rules.video_cache_hours(121), 336)

    def test_gradebook_page_size(self):
        self.assertEqual(rules.gradebook_page_size(0), 25)
        self.assertEqual(rules.gradebook_page_size(1), 25)
        self.assertEqual(rules.gradebook_page_size(30), 25)
        self.assertEqual(rules.gradebook_page_size(31), 50)
        self.assertEqual(rules.gradebook_page_size(150), 50)
        self.assertEqual(rules.gradebook_page_size(151), 100)
        self.assertEqual(rules.gradebook_page_size(600), 100)
        self.assertEqual(rules.gradebook_page_size(601), 200)

    def test_waitlist_size(self):
        self.assertEqual(rules.waitlist_size(0), 5)
        self.assertEqual(rules.waitlist_size(1), 5)
        self.assertEqual(rules.waitlist_size(20), 5)
        self.assertEqual(rules.waitlist_size(21), 20)
        self.assertEqual(rules.waitlist_size(100), 20)
        self.assertEqual(rules.waitlist_size(101), 50)
        self.assertEqual(rules.waitlist_size(500), 50)
        self.assertEqual(rules.waitlist_size(501), 100)

    def test_scholarship_credit_cap(self):
        self.assertEqual(rules.scholarship_credit_cap(0), 18)
        self.assertEqual(rules.scholarship_credit_cap(1), 18)
        self.assertEqual(rules.scholarship_credit_cap(2), 15)
        self.assertEqual(rules.scholarship_credit_cap(3), 12)
        self.assertEqual(rules.scholarship_credit_cap(4), 9)
