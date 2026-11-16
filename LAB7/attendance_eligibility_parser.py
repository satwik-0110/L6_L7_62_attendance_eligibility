"""Attendance eligibility input parser, hardened after fuzz testing.

Name: Satwik Subramanya   SRN: PES2UG24AM148   Section: AIML 5B

Every function accepts any input without raising an exception.
Input that cannot be understood returns None instead.
"""

# Longest whole number accepted in a ratio. No class count needs more
# digits, and it keeps int() away from absurdly long digit strings.
MAX_DIGITS = 6


def normalize_srn(srn):
    """
    Trims and upper-cases a student registration number.
    Returns None unless srn is a string that contains only English
    letters and digits once whitespace is removed.
    """
    if not isinstance(srn, str):
        return None
    cleaned = "".join(srn.split())
    if not cleaned or not cleaned.isascii() or not cleaned.isalnum():
        return None
    return cleaned.upper()


def _is_count(text):
    """True for a whole number written in plain digits, e.g. '30'."""
    return text.isascii() and text.isdigit() and len(text) <= MAX_DIGITS


def attendance_from_ratio(text):
    """
    Converts 'ATTENDED/HELD' into a whole-number percentage.
    Returns None unless text is two whole numbers separated by one '/',
    HELD is not zero and ATTENDED is not more than HELD.
    """
    if not isinstance(text, str):
        return None
    parts = [part.strip() for part in text.split('/')]
    if len(parts) != 2 or not all(_is_count(part) for part in parts):
        return None
    attended, held = int(parts[0]), int(parts[1])
    if held == 0 or attended > held:
        return None
    return attended * 100 // held


def attendance_from_register(marks):
    """
    Works out the attendance percentage from a string of P (present)
    and A (absent). Returns None unless marks is a string with at least
    one mark and nothing other than P or A (in either case).
    """
    if not isinstance(marks, str):
        return None
    marks = marks.strip()
    if not marks or not marks.isascii():
        return None
    marks = marks.upper()
    if set(marks) - {'P', 'A'}:
        return None
    return marks.count('P') * 100 // len(marks)


def _show(label, result):
    """Print a result, or a clear message when the input was not valid."""
    if result is None:
        print(label, "invalid input")
    else:
        print(label, result)


def main():
    print("==== Running normalize_srn ====")
    value = input("Enter an SRN (e.g. pes1ug23cs001): ")
    _show("Normalized SRN:", normalize_srn(value))

    print("\n==== Running attendance_from_ratio ====")
    value = input("Enter classes attended and held as ATTENDED/HELD (e.g. 30/40): ")
    _show("Attendance percent:", attendance_from_ratio(value))

    print("\n==== Running attendance_from_register ====")
    value = input("Enter the register as P/A marks (e.g. PPAPP): ")
    _show("Attendance percent:", attendance_from_register(value))


if __name__ == "__main__":
    main()
