import sqlite3
import re


def extract_sql(answer):
    """Extract SQL from a Markdown code block."""
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
    Evaluate the C05 SQL benchmark using
    an in-memory SQLite database.
    """
    query = extract_sql(answer)

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
            [
                (1, 101),
                (2, 102),
                (3, 103),
                (4, 104),
                (5, 105)
            ]
        )

        # Only allow a single SELECT statement.
        if not re.match(r"^\s*SELECT\b", query, re.I):
            return "needs_review"

        # Block multiple statements.
        if ";" in query.rstrip().rstrip(";"):
            return "needs_review"

        cursor = conn.execute(query)
        rows = cursor.fetchall()

        if rows == [(5,)]:
            return "correct"

        return "incorrect"

    except sqlite3.Error:
        return "incorrect"

    finally:
        conn.close()


if __name__ == "__main__":
    sample_answer = """
Here is the SQL query:

```sql
SELECT COUNT(*) FROM orders;
```
"""

    result = evaluate_sql(sample_answer)
    print("SQL evaluation result:", result)
