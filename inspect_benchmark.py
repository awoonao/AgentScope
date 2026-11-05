import sqlite3

conn = sqlite3.connect("agent_data.db")
conn.row_factory = sqlite3.Row

try:
    rows = conn.execute("""
        SELECT
            run_id,
            benchmark_id,
            prompt_id,
            status,
            answer
        FROM agent_runs
        WHERE prompt_id = ?
        ORDER BY run_id DESC
    """, ("C05",)).fetchall()

    if not rows:
        print("No records found for C05.")

    for row in rows:
        print("=" * 50)
        print("Run ID:", row["run_id"])
        print("Benchmark:", row["benchmark_id"])
        print("Prompt:", row["prompt_id"])
        print("Status:", row["status"])
        print("Gemini's answer:")
        print(row["answer"])
        print("=" * 50)

finally:
    conn.close()
