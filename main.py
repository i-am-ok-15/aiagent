import os
import sys

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

prompt_text = sys.argv[1]

print(prompt_text)

def gemini_prompt(prompt_text):
    if len(prompt_text) > 0:
        response = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt_text)
        print(f"Your response: {response.text}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    else:
        print("Error, invalid prompt")
        sys.exit(1)

gemini_prompt(prompt_text)

