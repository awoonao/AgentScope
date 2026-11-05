import os
import time
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types

from database import create_database, save_run, save_attempt


load_dotenv(".env")

PROVIDER = "google"
MODEL = "gemini-3.5-flash-lite"
AGENT_VERSION = "v2.1"

MAX_RETRIES = 2
BENCHMARK_MAX_RETRIES = 0
RETRY_DELAY = 2
REQUEST_TIMEOUT = 30000


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=REQUEST_TIMEOUT
    )
)


create_database()


def ask_agent(
    question,
    task_type=None,
    benchmark_id=None,
    prompt_id=None
):
    started_at = datetime.now()
    start_time = time.time()

    answer = None
    status = "failed"
    error_type = None
    error_message = None

    input_tokens = None
    output_tokens = None
    total_tokens = None

    retry_count = 0
    attempt_logs = []

    retryable_errors = {
        "ServerError",
        "ConnectError",
        "ReadError",
        "ConnectTimeout",
        "ReadTimeout",
        "TimeoutException"
    }

    max_retries = (
        BENCHMARK_MAX_RETRIES
        if benchmark_id is not None
        else MAX_RETRIES
    )

    for attempt in range(max_retries + 1):

        attempt_started_at = datetime.now()
        attempt_start_time = time.time()

        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=question
            )

            answer = response.text
            status = "success"

            error_type = None
            error_message = None

            if response.usage_metadata:
                input_tokens = (
                    response.usage_metadata.prompt_token_count
                )

                output_tokens = (
                    response.usage_metadata.candidates_token_count
                )

                total_tokens = (
                    response.usage_metadata.total_token_count
                )

            attempt_completed_at = datetime.now()
            attempt_duration = time.time() - attempt_start_time

            attempt_logs.append({
                "attempt_number": attempt + 1,
                "started_at": attempt_started_at.isoformat(),
                "completed_at": attempt_completed_at.isoformat(),
                "duration_seconds": attempt_duration,
                "status": "success",
                "error_type": None,
                "error_message": None
            })

            break

        except Exception as error:
            error_type = type(error).__name__
            error_message = str(error)

            attempt_completed_at = datetime.now()
            attempt_duration = time.time() - attempt_start_time

            attempt_logs.append({
                "attempt_number": attempt + 1,
                "started_at": attempt_started_at.isoformat(),
                "completed_at": attempt_completed_at.isoformat(),
                "duration_seconds": attempt_duration,
                "status": "failed",
                "error_type": error_type,
                "error_message": error_message
            })

            if (
                error_type in retryable_errors
                and attempt < max_retries
            ):
                retry_count += 1

                delay = RETRY_DELAY * (
                    2 ** (retry_count - 1)
                )

                print(
                    f"\nTemporary {error_type}. "
                    f"Retrying in {delay} seconds "
                    f"(retry {retry_count}/{max_retries})..."
                )

                time.sleep(delay)

            else:
                break


    completed_at = datetime.now()
    duration_seconds = time.time() - start_time

    run_id = save_run(
        question=question,
        answer=answer,
        provider=PROVIDER,
        model=MODEL,
        agent_version=AGENT_VERSION,
        task_type=task_type,
        benchmark_id=benchmark_id,
        prompt_id=prompt_id,
        started_at=started_at.isoformat(),
        completed_at=completed_at.isoformat(),
        duration_seconds=duration_seconds,
        status=status,
        error_type=error_type,
        error_message=error_message,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        retry_count=retry_count
    )

    for attempt_log in attempt_logs:
        save_attempt(
            run_id=run_id,
            attempt_number=attempt_log["attempt_number"],
            started_at=attempt_log["started_at"],
            completed_at=attempt_log["completed_at"],
            duration_seconds=attempt_log["duration_seconds"],
            status=attempt_log["status"],
            error_type=attempt_log["error_type"],
            error_message=attempt_log["error_message"]
        )


    if status == "success":
        return answer

    return f"Request failed: {error_message}"


if __name__ == "__main__":

    while True:
        question = input(
            "\nAsk the agent something "
            "(or type 'quit'): "
        )

        if question.lower() == "quit":
            break

        answer = ask_agent(question)

        print("\nAgent:")
        print(answer)