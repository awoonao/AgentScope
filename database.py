import sqlite3

DB_NAME = "agent_data.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,

            question TEXT NOT NULL,
            answer TEXT,

            provider TEXT NOT NULL,
            model TEXT NOT NULL,
            agent_version TEXT NOT NULL,

            started_at TEXT NOT NULL,
            completed_at TEXT NOT NULL,
            duration_seconds REAL NOT NULL,

            status TEXT NOT NULL,
            error_type TEXT,
            error_message TEXT,

            input_tokens INTEGER,
            output_tokens INTEGER,
            total_tokens INTEGER,

            retry_count INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_attempts (
            attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            attempt_number INTEGER NOT NULL,
            started_at TEXT NOT NULL,
            completed_at TEXT NOT NULL,
            duration_seconds REAL NOT NULL,
            status TEXT NOT NULL,
            error_type TEXT,
            error_message TEXT,
            FOREIGN KEY (run_id) REFERENCES agent_runs(run_id)
        )
    """)

    conn.commit()
    conn.close()

def save_run(
    question,
    answer,
    provider,
    model,
    agent_version,
    started_at,
    completed_at,
    duration_seconds,
    status,
    error_type=None,
    error_message=None,
    input_tokens=None,
    output_tokens=None,
    total_tokens=None,
    retry_count=0
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agent_runs (
            question,
            answer,
            provider,
            model,
            agent_version,
            started_at,
            completed_at,
            duration_seconds,
            status,
            error_type,
            error_message,
            input_tokens,
            output_tokens,
            total_tokens,
            retry_count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        question,
        answer,
        provider,
        model,
        agent_version,
        started_at,
        completed_at,
        duration_seconds,
        status,
        error_type,
        error_message,
        input_tokens,
        output_tokens,
        total_tokens,
        retry_count
    ))

    run_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return run_id

def save_attempt(
    run_id,
    attempt_number,
    started_at,
    completed_at,
    duration_seconds,
    status,
    error_type=None,
    error_message=None
):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agent_attempts (
            run_id,
            attempt_number,
            started_at,
            completed_at,
            duration_seconds,
            status,
            error_type,
            error_message
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        run_id,
        attempt_number,
        started_at,
        completed_at,
        duration_seconds,
        status,
        error_type,
        error_message
    ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database tables created successfully.")