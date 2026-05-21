import json
from unittest.mock import patch, MagicMock
from src.engine.engine import extract_vark_scores, reflect_on_scores, process_quiz_input

MOCK_SCORES = {"visual": 40, "auditory": 20, "reading": 25, "kinesthetic": 15}

def make_mock_model(scores=MOCK_SCORES):
    mock_response = MagicMock()
    mock_response.text = json.dumps(scores)
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    return mock_model

def test_extract_returns_all_vark_keys():
    with patch("src.engine.engine._get_client", return_value=make_mock_model()):
        result = extract_vark_scores("I love watching video tutorials and drawing diagrams.")
    assert result["status"] == "success"
    for key in ["visual", "auditory", "reading", "kinesthetic"]:
        assert key in result["data"]

def test_extract_returns_numeric_scores():
    with patch("src.engine.engine._get_client", return_value=make_mock_model()):
        result = extract_vark_scores("I prefer reading textbooks and writing detailed notes.")
    assert result["status"] == "success"
    assert all(isinstance(result["data"][k], (int, float)) for k in result["data"])

def test_reflect_complete_scores():
    scores = {"visual": 40, "auditory": 20, "reading": 25, "kinesthetic": 15}
    result = reflect_on_scores(scores)
    assert result["complete"] == True
    assert result["missing"] == []

def test_reflect_incomplete_scores():
    scores = {"visual": 40}
    result = reflect_on_scores(scores)
    assert result["complete"] == False
    assert "auditory" in result["missing"]

def test_process_quiz_input_success():
    with patch("src.engine.engine._get_client", return_value=make_mock_model()):
        result = process_quiz_input(
            "session_engine_001",
            "I always draw diagrams and watch videos. I rarely read textbooks."
        )
    assert result["status"] in ["success", "exists"]

def test_process_quiz_input_incomplete():
    incomplete = {"visual": 40}
    with patch("src.engine.engine._get_client", return_value=make_mock_model(incomplete)):
        result = process_quiz_input("session_engine_002", "I like things.")
    assert result["status"] in ["incomplete", "success", "exists"]