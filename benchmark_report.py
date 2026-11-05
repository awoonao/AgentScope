import sqlite3
import pandas as pd

DB_NAME = "agent_data.db"


def load_data():
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query("""
            SELECT
                run_id,
                benchmark_id,
                agent_version,
                model,
                prompt_id,
                task_type,
                status,
                duration_seconds,
                total_tokens,
                retry_count,
                error_type,
                error_message
            FROM agent_runs
            WHERE benchmark_id IS NOT NULL
            ORDER BY run_id
        """, conn)

    return df


def benchmark_summary(df):
    summary = (
        df.groupby(["benchmark_id", "model"])
        .agg(
            attempted=("run_id", "count"),
            successful=("status", lambda x: (x == "success").sum()),
            failed=("status", lambda x: (x == "failed").sum()),
            avg_latency=(
                "duration_seconds",
                lambda x: round(
                    x[df.loc[x.index, "status"] == "success"].mean(), 2
                )
            ),
            total_tokens=("total_tokens", "sum")
        )
        .reset_index()
    )

    summary["success_rate"] = (
        summary["successful"] / summary["attempted"] * 100
    ).round(1)

    return summary


def error_summary(df):
    errors = df[df["status"] == "failed"]

    return (
        errors.groupby(["benchmark_id", "error_type"])
        .size()
        .reset_index(name="count")
    )


def category_summary(df):
    summary = (
        df.groupby(["benchmark_id", "task_type"])
        .agg(
            attempted=("run_id", "count"),
            successful=("status", lambda x: (x == "success").sum())
        )
        .reset_index()
    )

    summary["success_rate"] = (
        summary["successful"] / summary["attempted"] * 100
    ).round(1)

    return summary


def classify_error(row):
    if row["status"] == "success":
        return "Success"

    message = str(row.get("error_message") or "")

    if "429" in message and "RESOURCE_EXHAUSTED" in message:
        return "Quota exhausted (429)"

    if "503" in message and "UNAVAILABLE" in message:
        return "Service unavailable (503)"

    if "504" in message and "DEADLINE_EXCEEDED" in message:
        return "Deadline exceeded (504)"

    if row["error_type"]:
        return str(row["error_type"])

    return "Unknown failure"


def main():
    df = load_data()

    df["error_category"] = df.apply(classify_error, axis=1)

    if df.empty:
        print("No benchmark data found.")
        return

    print("\n=== BENCHMARK COMPARISON ===")
    print(benchmark_summary(df).to_string(index=False))

    print("\n=== ERROR BREAKDOWN ===")
    print(error_summary(df).to_string(index=False))

    print("\n=== PERFORMANCE BY TASK CATEGORY ===")
    print(category_summary(df).to_string(index=False))

    print("\n=== DETAILED ERROR CATEGORIES ===")
    print(
        df[df["status"] == "failed"]
        .groupby(["benchmark_id", "error_category"])
        .size()
        .reset_index(name="count")
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
