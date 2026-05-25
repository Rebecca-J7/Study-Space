import uuid
from src.engine.engine import process_quiz_input
from src.engine.recommender import get_recommendations


def _progress_bar(percent: int, width: int = 20) -> str:
    filled = int(width * percent / 100)
    return "█" * filled + "░" * (width - filled)


def format_response(result: dict) -> str:
    status = result.get("status")

    if status == "success":
        scores = result.get("scores", {})
        dominant = result.get("dominant", "Unknown")

        # Build score display
        score_lines = "\n✅ Your VARK profile has been saved!\n\n📊 Your VARK Profile:\n"
        for style, score in scores.items():
            bar = _progress_bar(score)
            score_lines += f"   {style.capitalize():<14} {score:>3}%  {bar}\n"
        score_lines += f"\n   🏆 Dominant Style: {dominant} Learner\n"

        # Get recommendations
        vark_input = {**scores, "dominant": dominant}
        rec_result = get_recommendations(vark_input)

        rec_lines = "\n📚 Your Personalized Study Recommendations:\n"
        if rec_result["status"] in ["success", "tied"]:
            data = rec_result["data"]

            rec_lines += "\n   Core Strategies:\n"
            for tip in data["strategies"][:3]:
                rec_lines += f"   • {tip}\n"

            rec_lines += "\n   Recommended Tools:\n"
            for tool in data["tools"]:
                rec_lines += f"   • {tool}\n"

            if data.get("personalized_tips"):
                rec_lines += "\n   ✨ Personalized Tips Just for You:\n"
                for tip in data["personalized_tips"][:3]:
                    rec_lines += f"   • {tip}\n"

            if rec_result["status"] == "tied":
                tied = ", ".join(data["tied_styles"])
                rec_lines += f"\n   💡 Note: You have a tied profile ({tied})!\n"
        else:
            rec_lines += "   Could not generate recommendations at this time.\n"

        return score_lines + rec_lines

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

        context.append(user_input)
        combined_input = " ".join(context)

        if user_input.lower() in ["done", "finished", "results"]:
            if len(context) <= 1:
                print("\n⚠️  Please share something about yourself first!\n")
                continue
            combined_input = " ".join(context[:-1])
            print("\n🔍 Analyzing your learning style...\n")
            result = process_fn(session_id, combined_input)
            print(format_response(result))
            return

        print("\n🔍 Analyzing your learning style...\n")
        result = process_fn(session_id, combined_input)
        formatted = format_response(result)
        print(formatted)

        if result.get("status") in ["success", "exists", "error", "incomplete"]:
            return


if __name__ == "__main__":
    run_session()