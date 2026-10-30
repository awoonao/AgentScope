import sqlite3
import statistics

conn = sqlite3.connect("agent_data.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT DISTINCT agent_version
    FROM agent_runs
    ORDER BY agent_version
""")

versions = [row[0] for row in cursor.fetchall()]

print("\n========== AGENT PERFORMANCE ==========")

for version in versions:

    cursor.execute("""
        SELECT
            status,
            duration_seconds,
            total_tokens,
            retry_count,
            error_type
        FROM agent_runs
        WHERE agent_version = ?
    """, (version,))

    rows = cursor.fetchall()

    total = len(rows)

    successes = [r for r in rows if r[0] == "success"]
    failures = [r for r in rows if r[0] == "failed"]

    print(f"\n--- {version.upper()} ---")

    print(f"Total runs: {total}")

    print(
        f"Success: {len(successes)} "
        f"({len(successes) / total * 100:.1f}%)"
    )

    print(
        f"Failed: {len(failures)} "
        f"({len(failures) / total * 100:.1f}%)"
    )

    if successes:

        latencies = [r[1] for r in successes]

        print(
            f"Average successful latency: "
            f"{statistics.mean(latencies):.2f}s"
        )

        print(
            f"Median successful latency: "
            f"{statistics.median(latencies):.2f}s"
        )

        print(
            f"Min successful latency: "
            f"{min(latencies):.2f}s"
        )

        print(
            f"Max successful latency: "
            f"{max(latencies):.2f}s"
        )

        tokens = [
            r[2] for r in successes
            if r[2] is not None
        ]

        if tokens:
            print(
                f"Average tokens: "
                f"{statistics.mean(tokens):.2f}"
            )

    print(
        f"Total retries: "
        f"{sum(r[3] for r in rows)}"
    )

    if failures:

        error_counts = {}

        for row in failures:
            error = row[4]

            error_counts[error] = (
                error_counts.get(error, 0) + 1
            )

        print("Failure types:")

        for error, count in error_counts.items():
            print(f"  {error}: {count}")

conn.close()