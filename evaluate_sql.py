
import sqlite3
import re


def extract_sql(answer):
    """Extract SQL from a Markdown SQL code block."""
    match = re.search(
        r"```sql\s*(.*?)```",
        answer,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return answer.strip()


def evaluate_sql(answer):
    """
    Evaluate benchmark C05:
    Count the number of rows in an orders table.

    Returns:
        correct
        incorrect
        needs_review
    """

    query = extract_sql(answer)

    # Allow one SELECT statement only.
    if not re.match(r"^\s*SELECT\b", query, re.I):
        return "needs_review"

    # Reject multiple statements.
    if ";" in query.rstrip().rstrip(";"):
        return "needs_review"

    # Test against several different datasets.
    test_datasets = [
        [],
        [(1, 101)],
        [(1, 101), (2, 102), (3, 103)],
        [
            (1, 101),
            (2, 102),
            (3, None),
            (4, 104),
            (5, None)
        ]
    ]

    for dataset in test_datasets:
        conn = sqlite3.connect(":memory:")

        try:
            conn.execute("""
                CREATE TABLE orders (
                    order_id INTEGER PRIMARY KEY,
                    customer_id INTEGER
                )
            """)

            conn.executemany(
                "INSERT INTO orders VALUES (?, ?)",
                dataset
            )

            # Authorizer blocks non-read operations.
            def authorizer(action, arg1, arg2, db, source):
                allowed = {
                    sqlite3.SQLITE_SELECT,
                    sqlite3.SQLITE_READ,
                    sqlite3.SQLITE_FUNCTION
                }

                return (
                    sqlite3.SQLITE_OK
                    if action in allowed
                    else sqlite3.SQLITE_DENY
                )

            conn.set_authorizer(authorizer)

            # Interrupt excessively long queries.
            steps = [0]

            def progress_handler():
                steps[0] += 1
                return 1 if steps[0] > 100 else 0

            conn.set_progress_handler(progress_handler, 1000)

            cursor = conn.execute(query)
            rows = cursor.fetchall()

            expected = [(len(dataset),)]

            if rows != expected:
                return "incorrect"

        except sqlite3.Error:
            return "incorrect"

        finally:
            conn.close()

    return "correct"


if __name__ == "__main__":
    test_cases = [
        (
            "SELECT COUNT(*) FROM orders;",
            "correct"
        ),
        (
            "SELECT COUNT(order_id) FROM orders;",
            "correct"
        ),
        (
            "SELECT COUNT(customer_id) FROM orders;",
            "incorrect"
        ),
        (
            "SELECT 5;",
            "incorrect"
        ),
        (
            "SELECT COUNT(*) FROM orders WHERE order_id > 2;",
            "incorrect"
        ),
        (
            "DELETE FROM orders;",
            "needs_review"
        )
    ]

    passed = 0

    for query, expected in test_cases:
        result = evaluate_sql(query)
        success = result == expected

        if success:
            passed += 1

        print(f"\nSQL: {query}")
        print(f"Expected: {expected}")
        print(f"Actual: {result}")
        print(f"Test: {'PASS' if success else 'FAIL'}")

    print(f"\nTests passed: {passed}/{len(test_cases)}")
