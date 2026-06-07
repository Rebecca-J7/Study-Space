import pytest
from src.interface.cli import format_response, run_session, run_quiz, run_quiz_with_followup

# --- format_response tests ---

def test_format_unknown():
    result = {"status": "unknown"}
    output = format_response(result)
    assert "unexpected" in output.lower() or "?" in output

def test_format_success():
    result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 20, "reading": 10, "kinesthetic": 15},
        "dominant": "Visual"
    }
    output = format_response(result)
    assert "visual" in output.lower()
    assert "dominant" in output.lower()

def test_format_exists():
    result = {"status": "exists"}
    output = format_response(result)
    assert "already" in output.lower()

def test_format_incomplete():
    result = {"status": "incomplete", "missing": ["auditory", "kinesthetic"]}
    output = format_response(result)
    assert "auditory" in output
    assert "kinesthetic" in output

def test_format_error():
    result = {"status": "error", "message": "Something failed."}
    output = format_response(result)
    assert "wrong" in output.lower()

# --- run_session dependency injection tests ---

def test_run_session_success(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "I love watching videos and drawing diagrams.")
    mock_result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 20, "reading": 10, "kinesthetic": 15},
        "dominant": "Visual"
    }
    run_session(process_fn=lambda sid, inp: mock_result)
    captured = capsys.readouterr()
    assert "visual" in captured.out.lower()
    assert "dominant" in captured.out.lower()

def test_run_session_empty_input(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")
    run_session(process_fn=lambda sid, inp: {"status": "success"})
    captured = capsys.readouterr()
    assert "no input" in captured.out.lower()

def test_run_session_incomplete(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "I like things.")
    mock_result = {"status": "incomplete", "missing": ["visual", "auditory"]}
    run_session(process_fn=lambda sid, inp: mock_result)
    captured = capsys.readouterr()
    assert "visual" in captured.out.lower()

def test_format_low_confidence():
    result = {"status": "low_confidence", "confidence": 15, "message": "Input too vague."}
    output = format_response(result)
    assert "more" in output.lower() or "detail" in output.lower() or "vague" in output.lower()

def test_run_session_low_confidence_then_success(monkeypatch, capsys):
    """First response is low confidence, second is success — should loop and save."""
    responses = [
        {"status": "low_confidence", "confidence": 15, "message": "Too vague."},
        {
            "status": "success",
            "scores": {"visual": 55, "auditory": 20, "reading": 10, "kinesthetic": 15},
            "dominant": "Visual"
        }
    ]
    call_count = {"n": 0}

    def mock_process(sid, inp):
        result = responses[call_count["n"]]
        call_count["n"] += 1
        return result

    inputs = iter(["I like stuff.", "I love watching videos and drawing diagrams."])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_session(process_fn=mock_process)
    captured = capsys.readouterr()
    assert "visual" in captured.out.lower()

def test_run_session_quit_mid_session(monkeypatch, capsys):
    """User types quit after a low confidence response — should exit gracefully."""
    responses = [{"status": "low_confidence", "confidence": 15, "message": "Too vague."}]
    call_count = {"n": 0}

    def mock_process(sid, inp):
        result = responses[call_count["n"]]
        call_count["n"] += 1
        return result

    inputs = iter(["I like stuff.", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_session(process_fn=mock_process)
    captured = capsys.readouterr()
    assert "good luck" in captured.out.lower() or "bye" in captured.out.lower() or "quit" in captured.out.lower()

def test_run_session_done_forces_results(monkeypatch, capsys):
    """User types 'done' after low confidence — should force scoring with what's available."""
    responses = [
        {"status": "low_confidence", "confidence": 15, "message": "Too vague."},
        {"status": "success"}
    ]
    call_count = {"n": 0}

    def mock_process(sid, inp):
        result = responses[call_count["n"]]
        call_count["n"] += 1
        return result

    inputs = iter(["I like stuff.", "done"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    run_session(process_fn=mock_process)
    captured = capsys.readouterr()
    assert "saved" in captured.out.lower() or "profile" in captured.out.lower()

# --- Structured Quiz Flow Tests ---

def test_run_quiz_asks_multiple_questions(monkeypatch, capsys):
    """Quiz should ask all 5 questions before scoring."""
    answers = iter([
        "I prefer videos and diagrams.",
        "I write things down and draw.",
        "I like to see examples and charts.",
        "I prefer hands-on practice.",
        "I watch tutorials and take visual notes."
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    mock_result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
        "dominant": "Visual"
    }
    run_quiz(process_fn=lambda sid, inp: mock_result)
    captured = capsys.readouterr()
    assert "q1" in captured.out.lower() or "question 1" in captured.out.lower()
    assert "q5" in captured.out.lower() or "question 5" in captured.out.lower()
    assert "visual" in captured.out.lower()

def test_run_quiz_combines_all_answers(monkeypatch, capsys):
    """All 5 answers should be combined and passed to process_fn together."""
    collected_inputs = []

    def mock_process(sid, inp):
        collected_inputs.append(inp)
        return {
            "status": "success",
            "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
            "dominant": "Visual"
        }

    answers = iter([
        "I prefer videos.",
        "I write things down.",
        "I like charts.",
        "Hands-on practice.",
        "Visual notes."
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    run_quiz(process_fn=mock_process)

    assert len(collected_inputs) == 1
    combined = collected_inputs[0]
    assert "videos" in combined
    assert "charts" in combined
    assert "hands-on" in combined.lower()

def test_run_quiz_quit_mid_quiz(monkeypatch, capsys):
    """User can quit mid-quiz and session ends gracefully."""
    answers = iter(["I prefer videos.", "quit"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    run_quiz(process_fn=lambda sid, inp: {"status": "success"})
    captured = capsys.readouterr()
    assert "good luck" in captured.out.lower() or "bye" in captured.out.lower()

def test_run_quiz_empty_answer_skips(monkeypatch, capsys):
    """Empty answer on a question should re-prompt without skipping the question."""
    call_count = {"n": 0}
    answers = ["", "I prefer videos.", "I write things down.",
               "I like charts.", "Hands-on practice.", "Visual notes."]

    def mock_input(_):
        val = answers[call_count["n"]]
        call_count["n"] += 1
        return val

    monkeypatch.setattr("builtins.input", mock_input)
    mock_result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
        "dominant": "Visual"
    }
    run_quiz(process_fn=lambda sid, inp: mock_result)
    captured = capsys.readouterr()
    assert "visual" in captured.out.lower()

# --- Post-Results Q&A Tests ---

def test_followup_qa_after_results(monkeypatch, capsys):
    """After results, user can ask a follow-up question and get a response."""
    quiz_answers = iter([
        "I prefer videos.",
        "I write things down.",
        "I like charts.",
        "Hands-on practice.",
        "Visual notes.",
        "How should I study for exams?",  # follow-up question
        "done"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(quiz_answers))

    mock_result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
        "dominant": "Visual"
    }

    def mock_followup(question, dominant, scores):
        return "As a visual learner, try using color-coded summaries for exam review."

    run_quiz_with_followup(
        process_fn=lambda sid, inp: mock_result,
        followup_fn=mock_followup
    )
    captured = capsys.readouterr()
    assert "visual learner" in captured.out.lower() or "color" in captured.out.lower()

def test_followup_qa_done_exits(monkeypatch, capsys):
    """User types 'done' immediately after results — session ends gracefully."""
    quiz_answers = iter([
        "I prefer videos.",
        "I write things down.",
        "I like charts.",
        "Hands-on practice.",
        "Visual notes.",
        "done"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(quiz_answers))

    mock_result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
        "dominant": "Visual"
    }

    run_quiz_with_followup(
        process_fn=lambda sid, inp: mock_result,
        followup_fn=lambda q, d, s: "some answer"
    )
    captured = capsys.readouterr()
    assert "good luck" in captured.out.lower() or "bye" in captured.out.lower()

def test_followup_qa_multiple_questions(monkeypatch, capsys):
    """User can ask multiple follow-up questions before typing done."""
    quiz_answers = iter([
        "I prefer videos.",
        "I write things down.",
        "I like charts.",
        "Hands-on practice.",
        "Visual notes.",
        "How do I study for math?",
        "What about group study?",
        "done"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(quiz_answers))

    mock_result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
        "dominant": "Visual"
    }

    call_count = {"n": 0}
    def mock_followup(question, dominant, scores):
        call_count["n"] += 1
        return f"Answer {call_count['n']}"

    run_quiz_with_followup(
        process_fn=lambda sid, inp: mock_result,
        followup_fn=mock_followup
    )
    captured = capsys.readouterr()
    assert call_count["n"] == 2  # two follow-up questions asked

def test_followup_qa_quit_exits(monkeypatch, capsys):
    """User types quit during Q&A — exits gracefully."""
    quiz_answers = iter([
        "I prefer videos.",
        "I write things down.",
        "I like charts.",
        "Hands-on practice.",
        "Visual notes.",
        "quit"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(quiz_answers))

    mock_result = {
        "status": "success",
        "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
        "dominant": "Visual"
    }

    run_quiz_with_followup(
        process_fn=lambda sid, inp: mock_result,
        followup_fn=lambda q, d, s: "some answer"
    )
    captured = capsys.readouterr()
    assert "good luck" in captured.out.lower() or "bye" in captured.out.lower()

    # --- Vague Response Handling in run_quiz_with_followup ---

def test_run_quiz_low_confidence_prompts_elaboration(monkeypatch, capsys):
    """If all answers are vague, user is prompted to elaborate before scoring."""
    responses = [
        {"status": "low_confidence", "confidence": 20, "message": "Too vague."},
        {
            "status": "success",
            "scores": {"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20},
            "dominant": "Visual"
        }
    ]
    call_count = {"n": 0}

    def mock_process(sid, inp):
        result = responses[call_count["n"]]
        call_count["n"] += 1
        return result

    quiz_answers = iter([
        "I don't know.",      # Q1
        "Not sure.",          # Q2
        "I like things.",     # Q3
        "Maybe.",             # Q4
        "I guess notes.",     # Q5
        "I really love watching YouTube tutorials and drawing diagrams.",  # elaboration
        "done"                # end Q&A phase
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(quiz_answers))

    run_quiz_with_followup(
        process_fn=mock_process,
        followup_fn=lambda q, d, s: "some answer"
    )
    captured = capsys.readouterr()
    assert "vague" in captured.out.lower() or "detail" in captured.out.lower() or "elaborate" in captured.out.lower()


def test_run_quiz_low_confidence_done_forces_score(monkeypatch, capsys):
    """If confidence is low and user types 'done', score with what's available."""
    responses = [
        {"status": "low_confidence", "confidence": 20, "message": "Too vague."},
        {
            "status": "success",
            "scores": {"visual": 40, "auditory": 20, "reading": 20, "kinesthetic": 20},
            "dominant": "Visual"
        }
    ]
    call_count = {"n": 0}

    def mock_process(sid, inp):
        result = responses[call_count["n"]]
        call_count["n"] += 1
        return result

    quiz_answers = iter([
        "I don't know.",
        "Not sure.",
        "I like things.",
        "Maybe.",
        "I guess notes.",
        "done",   # force score
        "done"    # end Q&A phase
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(quiz_answers))

    run_quiz_with_followup(
        process_fn=mock_process,
        followup_fn=lambda q, d, s: "some answer"
    )
    captured = capsys.readouterr()
    assert "visual" in captured.out.lower() or "profile" in captured.out.lower()

def test_run_quiz_low_confidence_quit_exits(monkeypatch, capsys):
    """If confidence is low and user types 'quit', session ends gracefully."""
    responses = [
        {"status": "low_confidence", "confidence": 20, "message": "Too vague."},
    ]
    call_count = {"n": 0}

    def mock_process(sid, inp):
        result = responses[call_count["n"]]
        call_count["n"] += 1
        return result

    quiz_answers = iter([
        "I don't know.",
        "Not sure.",
        "I like things.",
        "Maybe.",
        "I guess notes.",
        "quit"
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(quiz_answers))

    run_quiz_with_followup(
        process_fn=mock_process,
        followup_fn=lambda q, d, s: "some answer"
    )
    captured = capsys.readouterr()
    assert "good luck" in captured.out.lower() or "bye" in captured.out.lower()