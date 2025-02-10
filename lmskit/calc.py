"""Composite charges built from the policy tables."""
from . import rules


def combined_charge(x):
    """Total of the two base schedules for x."""
    return rules.certificate_hours_required(x) + rules.plagiarism_similarity_limit_pct(x)
