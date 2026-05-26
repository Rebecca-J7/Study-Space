import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))


def run_agent(prompt: str) -> str:
    """Generate an agent response for the given prompt and return text.

    Returns the raw text from the model or raises an exception.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return getattr(response, "text", "")


if __name__ == "__main__":
    prompt = input("Paste your agent prompt here:\n> ")
    print("\n--- Gemini Agent Response ---\n")
    print(run_agent(prompt))
    print("\n--- End Response ---\n")