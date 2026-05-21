import uuid
from src.engine.engine import process_quiz_input


def format_response(result: dict) -> str:
    """Format the engine result dict into a human-readable string."""
    status = result.get("status")

    if status == "success":
        return (
            "\n✅ Your VARK profile has been saved!\n"
            "Check your personalized study recommendations below.\n"
        )
    elif status == "exists":
        return "\n⚠️  This session has already been recorded. No duplicate saved.\n"
    elif status == "incomplete":
        missing = result.get("missing", [])
        return (
            f"\n❌ Could not determine your full learning profile.\n"
            f"Missing scores for: {', '.join(missing)}\n"
            "Please try again with more detail about how you like to learn.\n"
        )
    elif status == "error":
        return f"\n❌ Something went wrong: {result.get('message', 'Unknown error')}\n"
    else:
        return f"\n❓ Unexpected response: {result}\n"


def run_session(process_fn=process_quiz_input):
    print("\n🎓 Welcome to Study Space!")
    print("=" * 40)
    print("I'll help you discover your learning style.")
    print("Type 'quit' or 'exit' to stop.\n")

    session_id = str(uuid.uuid4())

    print("Tell me about yourself as a learner.")
    print("For example: Do you prefer videos, reading, hands-on practice, or listening?\n")

    user_input = input("Your answer: ").strip()

    if not user_input:
        print("\n⚠️  No input provided. Please try again.\n")
        return

    if user_input.lower() in ["quit", "exit"]:
        print("\n👋 Thanks for using Study Space! Good luck studying!\n")
        return

    print("\n🔍 Analyzing your learning style...\n")

    result = process_fn(session_id, user_input)
    print(format_response(result))


if __name__ == "__main__":
    run_session()