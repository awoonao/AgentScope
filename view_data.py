import sqlite3

conn = sqlite3.connect("agent_data.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        run_id,
        provider,
        model,
        status,
        ROUND(duration_seconds, 2),
        input_tokens,
        output_tokens,
        total_tokens,
        retry_count,
        error_type
    FROM agent_runs
    ORDER BY run_id;
""")

rows = cursor.fetchall()

print("\n--- AGENT RUNS ---\n")

for row in rows:
    print(row)

conn.close()