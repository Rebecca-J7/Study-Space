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
    elif status == "low_confidence":
        confidence = result.get("confidence", 0)
        return (
            f"\n🤔 Your response was a bit vague (confidence: {confidence}%).\n"
            "Could you share more detail about how you like to learn?\n"
            "For example: Do you prefer videos, diagrams, reading, or hands-on practice?\n"
            "Type 'done' to get results with what you've shared, or 'quit' to exit.\n"
        )
    elif status == "error":
        return f"\n❌ Something went wrong: {result.get('message', 'Unknown error')}\n"
    else:
        return f"\n❓ Unexpected response: {result}\n"


def run_session(process_fn=process_quiz_input):
    """
    Run an interactive multi-turn VARK quiz session.
    Accepts process_fn for dependency injection (testable without real API).
    """
    print("\n🎓 Welcome to Study Space!")
    print("=" * 40)
    print("I'll help you discover your learning style.")
    print("Type 'quit' or 'exit' to stop.\n")

    session_id = str(uuid.uuid4())
    context = []

    print("Tell me about yourself as a learner.")
    print("For example: Do you prefer videos, reading, hands-on practice, or listening?\n")

    while True:
        user_input = input("Your answer: ").strip()

        if not user_input:
            print("\n⚠️  No input provided. Please try again.\n")
            return

        if user_input.lower() in ["quit", "exit"]:
            print("\n👋 Thanks for using Study Space! Good luck studying!\n")
            return

        # Accumulate context across turns
        context.append(user_input)
        combined_input = " ".join(context)

        # User signals they are done — force scoring with accumulated context
        if user_input.lower() in ["done", "finished", "results"]:
            if len(context) <= 1:
                print("\n⚠️  Please share something about yourself first!\n")
                continue
            # Use all previous context except the "done" signal
            combined_input = " ".join(context[:-1])
            print("\n🔍 Analyzing your learning style...\n")
            result = process_fn(session_id, combined_input)
            print(format_response(result))
            return

        print("\n🔍 Analyzing your learning style...\n")
        result = process_fn(session_id, combined_input)
        formatted = format_response(result)
        print(formatted)

        # If confident enough — done
        if result.get("status") in ["success", "exists", "error", "incomplete"]:
            return

        # If low confidence — loop and ask for more detail


if __name__ == "__main__":
    run_session()