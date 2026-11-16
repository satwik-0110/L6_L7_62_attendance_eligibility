"""Lab 6: branch coverage tests for attendance_eligibility.py.

Name: Satwik Subramanya   SRN: PES2UG24AM148   Section: AIML 5B

Run:
    coverage run --branch -m pytest test_attendance_eligibility.py
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


# =====================================================================
# Added for branch coverage
# =====================================================================

# ---------- attendance_percent: remaining branches ----------

def test_credited_attendance_cannot_exceed_total():
    # line 9 True branch: 38 attended + 5 leave = 43, capped to 40
    assert attendance_percent(38, 40, 5) == 100


def test_negative_total_is_rejected():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(0, -5, 0)


def test_negative_attended_is_rejected():
    # first half of "attended < 0 or attended > total_classes"
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 40, 0)


@pytest.mark.parametrize("leave, expected", [
    (4, 60),   # below the cap: 24 of 40
    (5, 62),   # exactly at the cap, not reduced: 25 of 40
    (6, 62),   # just over the cap, reduced to 5
])
def test_medical_leave_cap_boundary(leave, expected):
    assert attendance_percent(20, 40, leave) == expected


def test_percentage_is_rounded_down():
    assert attendance_percent(2, 3, 0) == 66


def test_full_and_zero_attendance():
    assert attendance_percent(40, 40, 0) == 100
    assert attendance_percent(0, 40, 0) == 0


# ---------- exam_eligibility: remaining branch and boundaries ----------

def test_condonation_required_without_condonation():
    # line 20 False branch: 65-74% and no condonation
    assert exam_eligibility(70, False, True) == "condonation required"


@pytest.mark.parametrize("percent, has_condonation, expected", [
    (75, False, "eligible"),               # lowest directly eligible value
    (74, False, "condonation required"),   # just below 75
    (74, True, "eligible"),
    (65, False, "condonation required"),   # lowest condonable value
    (65, True, "eligible"),
    (64, True, "detained"),                # just below 65
    (64, False, "detained"),
])
def test_eligibility_boundaries(percent, has_condonation, expected):
    assert exam_eligibility(percent, has_condonation, True) == expected


def test_fees_pending_is_checked_before_attendance():
    assert exam_eligibility(40, False, False) == "fees pending"


# ---------- attendance_warning: boundaries ----------

@pytest.mark.parametrize("percent, weeks_left, expected", [
    (85, 1, None),             # exactly 85: no warning
    (84, 1, "reminder"),       # just below 85
    (75, 10, "reminder"),      # exactly 75 is not "low"
    (74, 5, "critical"),       # just below 75, more than 4 weeks left
    (74, 4, "final notice"),   # exactly 4 weeks left is not "> 4"
    (0, 0, "final notice"),
])
def test_warning_boundaries(percent, weeks_left, expected):
    assert attendance_warning(percent, weeks_left) == expected
