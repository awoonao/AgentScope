import random
import sqlite3
import time

from app import ask_agent
from benchmark import BENCHMARK_ID, BENCHMARK_PROMPTS


DB_NAME = "agent_data.db"

DELAY_BETWEEN_PROMPTS = 5
RANDOM_SEED = 42


def get_completed_prompt_ids():
    """
    Return prompt IDs that have already been attempted
    for this benchmark and agent version.

    This allows the benchmark to resume without
    repeating prompts.
    """

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT prompt_id
        FROM agent_runs
        WHERE benchmark_id = ?
          AND prompt_id IS NOT NULL
    """, (BENCHMARK_ID,))

    completed = {row[0] for row in cursor.fetchall()}

    conn.close()

    return completed


def run_benchmark():

    completed_prompt_ids = get_completed_prompt_ids()

    remaining_prompts = [
        test
        for test in BENCHMARK_PROMPTS
        if test["prompt_id"] not in completed_prompt_ids
    ]

    random.seed(RANDOM_SEED)
    random.shuffle(remaining_prompts)

    print("\n========================================")
    print("AI AGENT BENCHMARK")
    print("========================================")

    print(f"Benchmark: {BENCHMARK_ID}")
    print(f"Total prompts: {len(BENCHMARK_PROMPTS)}")
    print(f"Already completed: {len(completed_prompt_ids)}")
    print(f"Remaining: {len(remaining_prompts)}")

    if not remaining_prompts:
        print("\nBenchmark already complete.")
        return

    for number, test in enumerate(remaining_prompts, start=1):

        prompt_id = test["prompt_id"]
        task_type = test["task_type"]
        prompt = test["prompt"]

        print("\n" + "=" * 60)
        print(
            f"PROMPT {number}/{len(remaining_prompts)} "
            f"({prompt_id})"
        )
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

        if number < len(remaining_prompts):
            print(
                f"\nWaiting {DELAY_BETWEEN_PROMPTS} seconds..."
            )
            time.sleep(DELAY_BETWEEN_PROMPTS)

    print("\n========================================")
    print("BENCHMARK COMPLETE")
    print("========================================")


if __name__ == "__main__":
    run_benchmark()