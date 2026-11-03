import sqlite3

DB_NAME = "agent_data.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(agent_runs)")
columns = [row[1] for row in cursor.fetchall()]

if "task_type" not in columns:
    cursor.execute("""
        ALTER TABLE agent_runs
        ADD COLUMN task_type TEXT
    """)
    print("Added task_type column.")
else:
    print("task_type column already exists.")


if "benchmark_id" not in columns:
    cursor.execute("""
        ALTER TABLE agent_runs
        ADD COLUMN benchmark_id TEXT
    """)
    print("Added benchmark_id column.")
else:
    print("benchmark_id column already exists.")


if "prompt_id" not in columns:
    cursor.execute("""
        ALTER TABLE agent_runs
        ADD COLUMN prompt_id TEXT
    """)
    print("Added prompt_id column.")
else:
    print("prompt_id column already exists.")


conn.commit()
conn.close()

print("Migration complete.")