
import sqlite3

conn = sqlite3.connect("agent_data.db")
conn.row_factory = sqlite3.Row

try:
    rows = conn.execute("""
        SELECT
            e.evaluation_id,
            e.run_id,
            r.benchmark_id,
            r.prompt_id,
            r.model,
            e.evaluation_result,
            e.evaluator_version,
            e.evaluated_at
        FROM answer_evaluations e
        JOIN agent_runs r
            ON e.run_id = r.run_id
        ORDER BY e.evaluation_id DESC
    """).fetchall()

    print("\n=== ANSWER EVALUATIONS ===")

    if not rows:
        print("No evaluations found.")

    for row in rows:
        print("-" * 40)
        for key in row.keys():
            print(f"{key}: {row[key]}")

    print("-" * 40)
    print(f"Total evaluations: {len(rows)}")

finally:
    conn.close()
