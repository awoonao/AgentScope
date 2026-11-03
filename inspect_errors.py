import sqlite3

conn = sqlite3.connect("agent_data.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        run_id,
        prompt_id,
        error_type,
        error_message
    FROM agent_runs
    WHERE run_id >= 29
    ORDER BY run_id
""")

rows = cursor.fetchall()

print("\n--- BENCHMARK ERRORS ---\n")

for row in rows:
    print(row)

conn.close()