
import random
import sqlite3
import time
import argparse

from app import ask_agent, AGENT_VERSION, MODEL
from benchmark import BENCHMARK_ID, BENCHMARK_PROMPTS


DB_NAME = "agent_data.db"

DELAY_BETWEEN_PROMPTS = 5
RANDOM_SEED = 42
MAX_CONSECUTIVE_SERVER_ERRORS = 2


def get_attempted_prompt_ids():
    """Return prompts already attempted for this benchmark."""

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT DISTINCT prompt_id
            FROM agent_runs
            WHERE benchmark_id = ?
              AND agent_version = ?
              AND model = ?
              AND prompt_id IS NOT NULL
        """, (BENCHMARK_ID, AGENT_VERSION, MODEL)).fetchall()

    return {row[0] for row in rows}


def get_latest_run(prompt_id):
    """Retrieve the latest database result for a prompt."""

    with sqlite3.connect(DB_NAME) as conn:
        return conn.execute("""
            SELECT status, error_type, error_message
            FROM agent_runs
            WHERE benchmark_id = ?
              AND agent_version = ?
              AND model = ?
              AND prompt_id = ?
            ORDER BY run_id DESC
            LIMIT 1
        """, (
            BENCHMARK_ID,
            AGENT_VERSION,
            MODEL,
            prompt_id
        )).fetchone()


def print_benchmark_summary():
    """Summarize the current benchmark results."""

    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT
                prompt_id,
                status,
                duration_seconds,
                total_tokens,
                error_type
            FROM agent_runs
            WHERE benchmark_id = ?
              AND agent_version = ?
              AND model = ?
              AND prompt_id IS NOT NULL
            ORDER BY run_id
        """, (BENCHMARK_ID, AGENT_VERSION, MODEL)).fetchall()

    # Use the latest result if a prompt has been attempted twice.
    latest_results = {row[0]: row for row in rows}

    results = list(latest_results.values())

    successes = [row for row in results if row[1] == "success"]
    failures = [row for row in results if row[1] == "failed"]

    attempted = len(results)
    total = len(BENCHMARK_PROMPTS)

    success_rate = (
        len(successes) / attempted * 100
        if attempted else 0
    )

    successful_latencies = [
        row[2] for row in successes if row[2] is not None
    ]

    avg_latency = (
        sum(successful_latencies) / len(successful_latencies)
        if successful_latencies else 0
    )

    total_tokens = sum(
        row[3] or 0 for row in successes
    )

    print("\n========================================")
    print("BENCHMARK SUMMARY")
    print("========================================")
    print(f"Benchmark:          {BENCHMARK_ID}")
    print(f"Model:              {MODEL}")
    print(f"Agent version:      {AGENT_VERSION}")
    print(f"Total prompts:      {total}")
    print(f"Attempted:          {attempted}")
    print(f"Successful:         {len(successes)}")
    print(f"Failed:             {len(failures)}")
    print(f"Not yet attempted:  {max(total - attempted, 0)}")
    print(f"Success rate:       {success_rate:.1f}%")
    print(f"Avg success latency:{avg_latency:8.2f}s")
    print(f"Success tokens:     {total_tokens}")
    print("========================================")


def run_benchmark(limit=5):

    attempted_prompt_ids = get_attempted_prompt_ids()

    remaining_prompts = [
        test
        for test in BENCHMARK_PROMPTS
        if test["prompt_id"] not in attempted_prompt_ids
    ]

    random.seed(RANDOM_SEED)
    random.shuffle(remaining_prompts)

    selected_prompts = remaining_prompts[:limit]

    print("\n========================================")
    print("AI AGENT BENCHMARK")
    print("========================================")
    print(f"Benchmark: {BENCHMARK_ID}")
    print(f"Model: {MODEL}")
    print(f"Total prompts: {len(BENCHMARK_PROMPTS)}")
    print(f"Already attempted: {len(attempted_prompt_ids)}")
    print(f"Selected this batch: {len(selected_prompts)}")

    if not selected_prompts:
        print("\nNo unattempted prompts remain.")
        print_benchmark_summary()
        return

    consecutive_server_errors = 0

    for number, test in enumerate(selected_prompts, start=1):

        prompt_id = test["prompt_id"]
        task_type = test["task_type"]
        prompt = test["prompt"]

        print("\n" + "=" * 60)
        print(f"PROMPT {number}/{len(selected_prompts)} ({prompt_id})")
        print(f"Task type: {task_type}")
        print(f"Question: {prompt}")
        print("=" * 60)

        answer = ask_agent(
            question=prompt,
            task_type=task_type,
            benchmark_id=BENCHMARK_ID,
            prompt_id=prompt_id
        )

        print("\nResult:")
        print(answer)

        result = get_latest_run(prompt_id)

        if result is None:
            print("\nWARNING: No database record found.")
            print("Stopping benchmark.")
            break

        status, error_type, error_message = result
        error_message = error_message or ""

        if status == "success":
            consecutive_server_errors = 0
            print("\nPrompt completed successfully.")

        elif status == "failed":

            if "429 RESOURCE_EXHAUSTED" in error_message:
                print("\nBENCHMARK STOPPED: API QUOTA EXHAUSTED")
                break

            elif (
                "503 UNAVAILABLE" in error_message
                or "504 DEADLINE_EXCEEDED" in error_message
            ):
                consecutive_server_errors += 1

                print(
                    "\nServer errors in a row:",
                    consecutive_server_errors
                )

                if (
                    consecutive_server_errors
                    >= MAX_CONSECUTIVE_SERVER_ERRORS
                ):
                    print("\nBENCHMARK STOPPED:")
                    print("Repeated server errors detected.")
                    break

            else:
                consecutive_server_errors = 0
                print(f"\nRequest failed: {error_type}")

        if number < len(selected_prompts):
            print(
                f"\nWaiting {DELAY_BETWEEN_PROMPTS} seconds..."
            )
            time.sleep(DELAY_BETWEEN_PROMPTS)

    print("\n========================================")
    print("BENCHMARK BATCH FINISHED")
    print("========================================")

    print_benchmark_summary()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of prompts to run"
    )

    args = parser.parse_args()

    if args.limit < 1:
        parser.error("--limit must be at least 1")

    run_benchmark(limit=args.limit)
