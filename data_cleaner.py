"""
Data Cleaner (pure Python, no external libraries)

clean_sensor_data(data) takes a list of mixed inputs and returns a list of
clean floats:
  - converts every element to float where possible
  - drops values that are None, cannot be converted, are negative, or are NaN/inf
  - caps any valid value above 500.0 to exactly 500.0
  - never crashes on empty, None, or fully invalid input
"""

import math

MAX_VALUE = 500.0


def clean_sensor_data(data):
    """Return a list of cleaned float readings from a list of mixed inputs."""
    if not data:  # handles None and empty list
        return []

    cleaned = []
    for item in data:
        if item is None or isinstance(item, bool):
            # bools are technically ints in Python; they are not sensor readings
            continue
        try:
            value = float(str(item).strip()) if isinstance(item, str) else float(item)
        except (ValueError, TypeError):
            continue

        if math.isnan(value) or math.isinf(value) or value < 0:
            continue

        cleaned.append(min(value, MAX_VALUE))
    return cleaned


if __name__ == "__main__":
    print("=" * 60)
    print("clean_sensor_data() test cases")
    print("=" * 60)

    # Test 1: mixed valid / invalid / negative / over-limit values
    test1 = [12, "45.5", None, "abc", -3, 750, " 99.9 ", [1, 2], 500.0001]
    result1 = clean_sensor_data(test1)
    print(f"\nTest 1 - Mixed inputs\n  Input : {test1}\n  Output: {result1}")
    assert result1 == [12.0, 45.5, 500.0, 99.9, 500.0], result1

    # Test 2: empty list
    test2 = []
    result2 = clean_sensor_data(test2)
    print(f"\nTest 2 - Empty list\n  Input : {test2}\n  Output: {result2}")
    assert result2 == []

    # Test 3: entirely invalid list
    test3 = [None, "N/A", -1, "", {}, float("nan"), "-0.5"]
    result3 = clean_sensor_data(test3)
    print(f"\nTest 3 - Entirely invalid list\n  Input : {test3}\n  Output: {result3}")
    assert result3 == []

    print("\nAll data cleaning tests passed.")
