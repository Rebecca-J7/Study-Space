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