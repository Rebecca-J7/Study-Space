# FUNCTIONALITY.md
---

## Functionality 1: Structured VARK Learning Style Quiz

- **Input:**
  - User's answers to 5 structured quiz questions asked by the system
  - Optional elaboration if initial answers are too vague (confidence below 40%)

- **Output:**
  - A learning style result (Visual, Auditory, Reading/Writing, or Kinesthetic) with a percentage breakdown
  - Dominant style identification
  - Session ID saved to Google Sheets with timestamp

- **Success:**
  - Gemini accurately scores all 5 combined responses and returns a clear dominant learning style profile with confidence above 40%
  - Result is saved to Google Sheets without error

- **Failure/Edge Cases:**
  - User gives vague/off-topic answers → confidence check triggers, system prompts for elaboration before scoring
  - User skips a question or inputs nothing → prompt user to answer before continuing to next question
  - Confidence remains low after elaboration → user can type `done` to force scoring or `quit` to exit
  - Duplicate session ID → storage returns `"exists"`, no duplicate row written to Sheets
  - Missing VARK keys in extraction → reflection returns `"incomplete"`, storage is never called

---

## Functionality 2: Personalized Study Method Recommendations

- **Input:**
  - The user's VARK quiz result (scores and dominant style)

- **Output:**
  - A tailored list of study strategies matched to their learning style
  - A list of recommended tools
  - Gemini-generated personalized tips based on the user's exact score profile

- **Success:**
  - Hardcoded strategies and tools are returned for the dominant VARK style
  - Gemini generates 3 personalized tips specific to the user's exact score breakdown
  - Recommendations display immediately after quiz results without a separate user action

- **Failure/Edge Cases:**
  - Mixed/tied results → suggest strategies from both tied modalities, note the tie in output
  - Gemini API unavailable → hardcoded strategies and tools still display, personalized tips section is skipped gracefully
  - Missing dominant key in input → return `{"status": "error", "message": "Could not generate recommendations."}`

---

## Functionality 3: Post-Results Q&A Session

- **Input:**
  - Free-text follow-up questions from the user about their learning style or study tips
  - User's dominant style and VARK scores (carried from quiz result)

- **Output:**
  - Gemini-generated 2–3 sentence personalized response to each question
  - Session ends when user types `done`, `finished`, or `quit`

- **Success:**
  - Gemini answers each question with advice specific to the user's dominant style and exact score profile
  - User can ask multiple questions before ending the session
  - Clean exit with goodbye message on `done` or `quit`

- **Failure/Edge Cases:**
  - Empty question input → return fallback prompt asking user to type a question
  - Gemini API error → return friendly error message, allow user to retry
  - Off-topic question → Gemini redirects toward study-related advice

---

## Functionality 4: Quiz Retake & Session Reset

- **Input:**
  - User clicks "Start New Session" button

- **Output:**
  - All session state cleared (session ID, messages, scores, phase)
  - Quiz restarted from the welcome screen with a fresh session ID

- **Success:**
  - UI resets cleanly to the welcome screen with "Start Quiz" button
  - New UUID generated for the next session
  - Previous session data remains in Google Sheets for historical record

- **Failure/Edge Cases:**
  - User accidentally clicks reset mid-quiz → state clears immediately, no confirmation required (new session ID means no data loss in Sheets)
  - Page refresh mid-quiz → session state lost, user must start over from the beginning
