import sqlite3

from evaluate_answers import evaluate_answer

DB_PATH = "agent_data.db"
EVALUATOR_VERSION = "rule_based_v1"

# Only evaluate prompts with verified expected answers.
# Add entries here when their benchmark prompt IDs
# and expected answers have been checked.
EXPECTED_ANSWERS = {}


def save_evaluations():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        rows = conn.execute("""
            SELECT run_id, prompt_id, answer
            FROM agent_runs
            WHERE status = 'success'
              AND prompt_id IS NOT NULL
              AND answer IS NOT NULL
        """).fetchall()

        saved = 0

        for row in rows:
            expected = EXPECTED_ANSWERS.get(row["prompt_id"])

            if expected is None:
                continue

            result = evaluate_answer(
                row["answer"],
                expected
            )

            conn.execute("""
                INSERT OR IGNORE INTO answer_evaluations (
                    run_id,
                    expected_answer,
                    evaluation_result,
                    evaluator_version
                )
                VALUES (?, ?, ?, ?)
            """, (
                row["run_id"],
                expected,
                result,
                EVALUATOR_VERSION
            ))

            saved += 1

        conn.commit()

        print(f"Eligible evaluations processed: {saved}")

        total = conn.execute("""
            SELECT COUNT(*)
            FROM answer_evaluations
            WHERE evaluator_version = ?
        """, (EVALUATOR_VERSION,)).fetchone()[0]

        print(f"Total stored evaluations: {total}")

    finally:
        conn.close()


if __name__ == "__main__":
    save_evaluations()
