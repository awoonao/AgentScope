import sqlite3

from evaluate_sql import evaluate_sql

DB_PATH = "agent_data.db"
EVALUATOR_VERSION = "sql_execution_v2"


def save_sql_evaluation():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        # Find the successful C05 benchmark response.
        row = conn.execute("""
            SELECT run_id, answer
            FROM agent_runs
            WHERE benchmark_id = ?
              AND prompt_id = ?
              AND status = 'success'
            ORDER BY run_id DESC
            LIMIT 1
        """, ("benchmark_v3", "C05")).fetchone()

        if row is None:
            print("No successful C05 response found.")
            return

        result = evaluate_sql(row["answer"])

        conn.execute("""
            INSERT INTO answer_evaluations (
                run_id,
                expected_answer,
                evaluation_result,
                evaluator_version
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(run_id, evaluator_version)
            DO UPDATE SET
                expected_answer = excluded.expected_answer,
                evaluation_result = excluded.evaluation_result,
                evaluated_at = CURRENT_TIMESTAMP
        """, (
            row["run_id"],
            "COUNT(*) FROM orders",
            result,
            EVALUATOR_VERSION
        ))

        conn.commit()

        print("Evaluation saved successfully!")
        print("Run ID:", row["run_id"])
        print("Evaluation result:", result)
        print("Evaluator version:", EVALUATOR_VERSION)

    finally:
        conn.close()


if __name__ == "__main__":
    save_sql_evaluation()
