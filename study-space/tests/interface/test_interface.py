import pytest
from src.interface.cli import format_response, run_session

# --- format_response tests ---

def test_format_unknown():
    result = {"status": "unknown"}
    output = format_response(result)
    assert "unexpected" in output.lower() or "?" in output

def test_format_success():
    result = {"status": "success"}
    output = format_response(result)
    assert "saved" in output.lower()

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
    mock_result = {"status": "success"}
    run_session(process_fn=lambda sid, inp: mock_result)
    captured = capsys.readouterr()
    assert "saved" in captured.out.lower()

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
        {"status": "success"}
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
    assert "saved" in captured.out.lower()

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