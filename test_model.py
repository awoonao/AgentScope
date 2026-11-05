import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000)
)

MODEL = "gemini-3.5-flash-lite"

try:
    response = client.models.generate_content(
        model=MODEL,
        contents="What is 5 + 5?"
    )

    print("Model:", MODEL)
    print("Response:", response.text)
    print("Status: SUCCESS")

except Exception as e:
    print("Model:", MODEL)
    print("Status: FAILED")
    print("Error:", str(e))