"""Lab 7: Hypothesis fuzz tests for attendance_eligibility_parser.py.

Name: Satwik Subramanya   SRN: PES2UG24AM148   Section: AIML 5B

Each test states two properties and lets Hypothesis look for an input
that breaks them:
  1. the function never raises, whatever it is given;
  2. when it returns a value, that value is sensible
     (a clean SRN, or a percentage between 0 and 100).
A return value of None means "this input is not valid".

Run:
    pytest test_attendance_eligibility_parser.py
"""
from hypothesis import given, strategies as st
from attendance_eligibility_parser import (
    normalize_srn,
    attendance_from_ratio,
    attendance_from_register,
)

# Values that are not text at all. The functions were written assuming str.
other_types = (
    st.integers() | st.floats() | st.booleans() | st.binary()
    | st.lists(st.integers())
)

# Text shaped like "ATTENDED/HELD". Plain random text almost never contains
# two numbers around a slash, so this gets the fuzzer as far as the
# arithmetic: zero held, negative numbers and attended greater than held.
ratio_like = st.builds(
    "{}/{}".format, st.integers(-5, 500), st.integers(-5, 500)
)

# Registers made mostly of real marks, mixed with spaces and stray characters.
register_like = st.text(alphabet="PApa xX1\t\n", max_size=40)


@given(st.text() | st.none() | other_types)
def test_normalize_srn_no_crash(s):
    try:
        result = normalize_srn(s)
    except Exception as e:
        assert False, f"normalize_srn crashed with: {e!r}"
    if result is not None:
        assert isinstance(result, str), f"not a string: {result!r}"
        assert result.isascii() and result.isalnum(), f"not clean: {result!r}"
        assert result == result.upper(), f"not upper-case: {result!r}"


@given(st.text() | st.none() | other_types | ratio_like)
def test_attendance_from_ratio_no_crash(s):
    try:
        result = attendance_from_ratio(s)
    except Exception as e:
        assert False, f"attendance_from_ratio crashed with: {e!r}"
    if result is not None:
        assert isinstance(result, int), f"not a whole number: {result!r}"
        assert 0 <= result <= 100, f"percentage out of range: {result!r}"


@given(st.text() | st.none() | other_types | register_like)
def test_attendance_from_register_no_crash(s):
    try:
        result = attendance_from_register(s)
    except Exception as e:
        assert False, f"attendance_from_register crashed with: {e!r}"
    if result is not None:
        assert isinstance(result, int), f"not a whole number: {result!r}"
        assert 0 <= result <= 100, f"percentage out of range: {result!r}"
        # Every valid mark is P or A, so the result must match a recount.
        marks = s.strip().upper()
        assert set(marks) <= {"P", "A"}, f"accepted invalid marks: {s!r}"
        assert result == marks.count("P") * 100 // len(marks)
