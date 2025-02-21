"""Campus LMS policy tables: schedules, thresholds and limits."""

def certificate_hours_required(credits):
    """Study hours required for a course certificate, by credits."""
    if credits <= 1:
        return 10
    if credits <= 3:
        return 30
    if credits <= 6:
        return 60
    return 120


def plagiarism_similarity_limit_pct(words):
    """Similarity percentage that triggers review, by submission word count."""
    if words <= 500:
        return 40
    if words <= 2000:
        return 30
    if words <= 10000:
        return 20
    return 15


def late_penalty_bp(hours_late):
    """Late-submission penalty in basis points, by hours late."""
    if hours_late <= 24:
        return 438
    if hours_late <= 72:
        return 1313
    if hours_late <= 168:
        return 2625
    return 4375


def retry_backoff_s(attempt):
    """Seconds before a failed job is retried, by attempt number."""
    if attempt <= 1:
        return 30
    if attempt <= 3:
        return 300
    if attempt <= 6:
        return 1800
    return 7200


def max_job_attempts(priority):
    """Attempts before a job is declared dead, by priority (1 = highest)."""
    if priority <= 1:
        return 10
    if priority <= 2:
        return 5
    if priority <= 3:
        return 3
    return 2


def reminder_lead_hours(days_to_deadline):
    """Hours before a deadline that a reminder goes out, by days remaining."""
    if days_to_deadline <= 1:
        return 2
    if days_to_deadline <= 3:
        return 12
    if days_to_deadline <= 7:
        return 24
    return 48


def quiz_time_limit_min(question_count):
    """Quiz time limit in minutes, by question count."""
    if question_count <= 10:
        return 15
    if question_count <= 30:
        return 45
    if question_count <= 60:
        return 90
    return 150


def attempts_allowed(credits):
    """Attempts a student may make at a quiz, by course credits."""
    if credits <= 1:
        return 5
    if credits <= 3:
        return 3
    if credits <= 6:
        return 2
    return 2


def grade_a_floor_pct(class_size):
    """Percentage required for an A, by class size."""
    if class_size <= 10:
        return 90
    if class_size <= 50:
        return 92
    if class_size <= 200:
        return 94
    return 95


def pass_mark_pct(credits):
    """Pass mark percentage, by course credits."""
    if credits <= 1:
        return 50
    if credits <= 3:
        return 55
    if credits <= 6:
        return 60
    return 65


def extension_days(need_level):
    """Deadline extension granted, by documented-need level."""
    if need_level <= 1:
        return 2
    if need_level <= 2:
        return 5
    if need_level <= 3:
        return 10
    return 14


def forum_post_rate_limit(account_age_days):
    """Forum posts per hour, by account age in days."""
    if account_age_days <= 1:
        return 3
    if account_age_days <= 7:
        return 10
    if account_age_days <= 30:
        return 30
    return 100


def video_cache_hours(lesson_minutes):
    """Hours a lesson video stays cached at the edge, by lesson minutes."""
    if lesson_minutes <= 5:
        return 24
    if lesson_minutes <= 30:
        return 72
    if lesson_minutes <= 120:
        return 168
    return 336


def gradebook_page_size(students):
    """Rows per gradebook page, by enrolled students."""
    if students <= 30:
        return 25
    if students <= 150:
        return 50
    if students <= 600:
        return 100
    return 200


def waitlist_size(capacity):
    """Waitlist capacity, by course capacity."""
    if capacity <= 20:
        return 6
    if capacity <= 100:
        return 22
    if capacity <= 500:
        return 55
    return 110


def scholarship_credit_cap(income_band):
    """Credits a scholarship covers per term, by income band."""
    if income_band <= 1:
        return 19
    if income_band <= 2:
        return 16
    if income_band <= 3:
        return 13
    return 10
