import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def run_agent(prompt: str):
    print("\n--- Gemini Agent Response ---\n")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    print(response.text)
    print("\n--- End Response ---\n")

if __name__ == "__main__":
    prompt = input("Paste your agent prompt here:\n> ")
    run_agent(prompt)