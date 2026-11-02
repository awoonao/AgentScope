import sqlite3

conn = sqlite3.connect("agent_data.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT
        a.attempt_id,
        a.run_id,
        r.agent_version,
        a.attempt_number,
        a.status,
        ROUND(a.duration_seconds, 2),
        a.error_type
    FROM agent_attempts a
    JOIN agent_runs r
        ON a.run_id = r.run_id
    ORDER BY a.attempt_id
""")

rows = cursor.fetchall()

print("\n--- AGENT ATTEMPTS ---\n")

for row in rows:
    print(row)

conn.close()