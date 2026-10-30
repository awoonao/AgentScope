import os
import time
from datetime import datetime

from dotenv import load_dotenv
from google import genai

from database import create_database, save_run


load_dotenv(".env")

PROVIDER = "google"
MODEL = "gemini-3.8-flash"
AGENT_VERSION = "v1"

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)

create_database()


def ask_agent(question):
    started_at = datetime.now()
    start_time = time.time()

    answer = None
    status = "failed"
    error_type = None
    error_message = None

    input_tokens = None
    output_tokens = None
    total_tokens = None

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=question
        )

        answer = response.text
        status = "success"

        # Gemini usage metadata
        if response.usage_metadata:
            input_tokens = response.usage_metadata.prompt_token_count
            output_tokens = response.usage_metadata.candidates_token_count
            total_tokens = response.usage_metadata.total_token_count

    except Exception as error:
        error_type = type(error).__name__
        error_message = str(error)

    completed_at = datetime.now()
    duration_seconds = time.time() - start_time

    save_run(
        question=question,
        answer=answer,
        provider=PROVIDER,
        model=MODEL,
        agent_version=AGENT_VERSION,
        started_at=started_at.isoformat(),
        completed_at=completed_at.isoformat(),
        duration_seconds=duration_seconds,
        status=status,
        error_type=error_type,
        error_message=error_message,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        retry_count=0
    )

    if status == "success":
        return answer

    return f"Request failed: {error_message}"


while True:
    question = input("\nAsk the agent something (or type 'quit'): ")

    if question.lower() == "quit":
        break

    answer = ask_agent(question)

    print("\nAgent:")
    print(answer)