# FUNCTIONALITY.md

## Purpose
Define what the system should do, i.e., functionalities.

### Functionality 1: VARK Learning Style Quiz
- Input:
  - User's answers to conversational quiz questions asked by Gemini
- Output:
  - A learning style result (Visual, Auditory, Reading/Writing, or Kinesthetic) with a percentage breakdown
- Success:
  - Gemini accurately scores responses and returns a clear dominant learning style profile
- Failure/Edge Cases: 
  - User gives vague/off-topic answers → Gemini asks a clarifying follow-up question
  - User skips a question or inputs nothing → prompt user to answer before continuing

### Functionality 2: Personalized Study Method Recommendations
- Input:
  - The user's VARK quiz result
- Output:
  - A tailored list of study strategies and tool suggestions matched to their learning style
- Success:
  - Recommendations are specific and relevant (e.g., mind maps for Visual, voice memos for Auditory)
- Failure/Edge Cases:
  - Mixed/tied results → suggest strategies from both tied modalities
  - Gemini returns a generic response → system re-prompts with more specific context

### Functionality 3: Quiz Retake & Profile Reset
- Input:
  - User requests to retake the quiz or start over
- Output:
  - Clears previous results and restarts the VARK quiz from the beginning
- Success:
  - Session resets cleanly and Gemini greets the user as if starting fresh
- Failure/Edge Cases:
  - User accidentally hits retake → confirm with "Are you sure? This will clear your current results."
  - Page refresh mid-quiz → warn user that progress may be lost
