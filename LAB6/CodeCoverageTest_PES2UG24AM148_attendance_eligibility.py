"""Lab 6: code (line) coverage tests for attendance_eligibility.py.

Name: Satwik Subramanya   SRN: PES2UG24AM148   Section: AIML 5B

Run:
    coverage run -m pytest CodeCoverageTest_PES2UG24AM148_attendance_eligibility.py
    coverage report -m
"""
import pytest
from attendance_eligibility import (
    attendance_percent,
    exam_eligibility,
    attendance_warning,
)


# ---------- attendance_percent ----------

def test_plain_percent():
    assert attendance_percent(30, 40, 0) == 75


def test_total_classes_must_be_positive():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, 0, 0)


def test_attended_cannot_exceed_total():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(41, 40, 0)


def test_medical_leave_is_capped_at_five_days():
    # 20 attended + 9 leave days is credited as 20 + 5 = 25 of 40
    assert attendance_percent(20, 40, 9) == 62


# ---------- exam_eligibility ----------

def test_eligible():
    assert exam_eligibility(80, False, True) == "eligible"


def test_fees_pending_overrides_good_attendance():
    assert exam_eligibility(95, True, False) == "fees pending"


def test_condonation_makes_borderline_student_eligible():
    assert exam_eligibility(70, True, True) == "eligible"


def test_detained_below_65_even_with_condonation():
    assert exam_eligibility(50, True, True) == "detained"


# ---------- attendance_warning ----------

def test_no_warning_for_high_attendance():
    assert attendance_warning(90, 3) is None


def test_reminder_between_75_and_84():
    assert attendance_warning(80, 3) == "reminder"


def test_critical_when_low_with_weeks_left():
    assert attendance_warning(60, 6) == "critical"


def test_final_notice_when_low_and_term_almost_over():
    assert attendance_warning(60, 2) == "final notice"
