import sqlite3

conn = sqlite3.connect("agent_data.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        run_id,
        agent_version,
        benchmark_id,
        prompt_id,
        task_type,
        status,
        ROUND(duration_seconds, 2),
        total_tokens,
        retry_count,
        error_type
    FROM agent_runs
    ORDER BY run_id
""")
rows = cursor.fetchall()

print("\n--- AGENT RUNS ---\n")

for row in rows:
    print(row)

conn.close()