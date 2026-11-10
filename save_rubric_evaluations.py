
import sqlite3

DB_NAME = "agent_data.db"
RUBRIC_VERSION = "rubric_v1"

evaluations = [
    (94, "relevance", 2, "Thanks the repeat customer"),
    (94, "brevity", 1, "Provides three options instead of one"),
    (94, "tone", 2, "Friendly and professional"),

    (98, "relevance", 2, "Relevant checkout improvements"),
    (98, "completeness", 2, "Three distinct suggestions"),
    (98, "actionability", 2, "Practical implementation steps")
]


def save_rubric_evaluations():
    conn = sqlite3.connect(DB_NAME)

    try:
        for run_id, criterion, score, notes in evaluations:
            # Ensure the run exists and was successful.
            run = conn.execute("""
                SELECT run_id
                FROM agent_runs
                WHERE run_id = ?
                  AND status = 'success'
            """, (run_id,)).fetchone()

            if run is None:
                print(f"Skipping run {run_id}: no successful run found")
                continue

            conn.execute("""
                INSERT INTO rubric_evaluations (
                    run_id,
                    criterion,
                    score,
                    max_score,
                    evaluator_type,
                    rubric_version,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_id, criterion, rubric_version)
                DO UPDATE SET
                    score = excluded.score,
                    notes = excluded.notes,
                    evaluated_at = CURRENT_TIMESTAMP
            """, (
                run_id,
                criterion,
                score,
                2,
                "assistant_review",
                RUBRIC_VERSION,
                notes
            ))

        conn.commit()
        print("Rubric evaluations saved successfully!")

        for run_id in (94, 98):
            result = conn.execute("""
                SELECT
                    SUM(score),
                    SUM(max_score)
                FROM rubric_evaluations
                WHERE run_id = ?
                  AND rubric_version = ?
            """, (run_id, RUBRIC_VERSION)).fetchone()

            print(
                f"Run {run_id}: {result[0]}/{result[1]}"
            )

    finally:
        conn.close()


if __name__ == "__main__":
    save_rubric_evaluations()
