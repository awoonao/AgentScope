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
            benchmark_id TEXT,
            prompt_id TEXT,
            task_type TEXT,

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
    task_type,
    benchmark_id,
    prompt_id,
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
            task_type,
            benchmark_id,
            prompt_id,
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        question,
        answer,
        provider,
        model,
        agent_version,
        task_type,
        benchmark_id,
        prompt_id,
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


def create_evaluations_table():
    """Create a separate table for answer evaluations."""
    import sqlite3

    conn = sqlite3.connect("agent_data.db")

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS answer_evaluations (
                evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                expected_answer TEXT NOT NULL,
                evaluation_result TEXT NOT NULL
                    CHECK (
                        evaluation_result IN (
                            'correct',
                            'incorrect',
                            'needs_review'
                        )
                    ),
                evaluator_version TEXT NOT NULL,
                evaluated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(run_id, evaluator_version)
            )
        """)

        conn.commit()
        print("Answer evaluations table ready.")

    finally:
        conn.close()


def create_rubric_evaluations_table():
    """Create a table for human-reviewed rubric scores."""
    import sqlite3

    conn = sqlite3.connect("agent_data.db")

    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rubric_evaluations (
                rubric_evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id INTEGER NOT NULL,
                criterion TEXT NOT NULL,
                score INTEGER NOT NULL
                    CHECK (score BETWEEN 0 AND 2),
                max_score INTEGER NOT NULL DEFAULT 2,
                evaluator_type TEXT NOT NULL,
                rubric_version TEXT NOT NULL,
                notes TEXT,
                evaluated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(run_id, criterion, rubric_version)
            )
        """)

        conn.commit()
        print("Rubric evaluations table ready.")

    finally:
        conn.close()


if __name__ == "__main__":
    create_database()
    print("Database tables created successfully.")

    create_evaluations_table()
    create_rubric_evaluations_table()