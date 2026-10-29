
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY missing. Check your .env file.")

client = genai.Client(api_key=api_key)

for attempt in range(1, 4):
    try:
        print(f"Attempt {attempt}/3...")

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents="Explain RAG in two simple sentences."
        )

        print("\nGemini connection successful!")
        print("\nAnswer:")
        print(response.text)
        break

    except Exception as error:
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")

        if attempt < 3:
            wait_seconds = attempt * 5
            print(f"Retrying in {wait_seconds} seconds...")
            time.sleep(wait_seconds)
        else:
            print("All attempts failed. We can retry later.")
