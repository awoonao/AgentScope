
from evaluate_answers import evaluate_answer


test_cases = [
    ("5 + 5 = 10", "10", "correct"),
    ("12 multiplied by 4 equals 48", "48", "correct"),
    ("The capital of France is Paris.", "Paris", "correct"),
    ("The square root of 81 is 9.", "9", "correct"),
    ("100 divided by 4 equals 25.", "25", "correct"),

    ("The answer is not 10.", "10", "needs_review"),
    ("The answer is 100.", "10", "incorrect"),
    ("The answer is 10.", "10", "correct"),
    ("The answer could be 10 or 11.", "10", "needs_review"),
    ("Paris is not the capital of France.", "Paris", "needs_review"),
]

passed = 0

for actual, expected, expected_result in test_cases:
    result = evaluate_answer(actual, expected)
    success = result == expected_result

    if success:
        passed += 1

    print(f"Answer: {actual}")
    print(f"Expected: {expected_result}")
    print(f"Actual: {result}")
    print(f"Test: {'PASS' if success else 'FAIL'}")
    print("-" * 40)

print(f"\nTests passed: {passed}/{len(test_cases)}")
