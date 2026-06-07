import json
from unittest.mock import patch, MagicMock
from src.engine.engine import extract_vark_scores, reflect_on_scores, process_quiz_input, answer_followup

MOCK_SCORES = {"visual": 40, "auditory": 20, "reading": 25, "kinesthetic": 15, "confidence": 85}

def make_mock_model(scores=None):
    if scores is None:
        scores = MOCK_SCORES
    mock_response = MagicMock()
    mock_response.text = json.dumps(scores)  # must be a real string
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    return mock_model

def make_mock_client_low_confidence():
    low_conf_scores = {"visual": 25, "auditory": 25, "reading": 25, "kinesthetic": 25, "confidence": 15}
    mock_response = MagicMock()
    mock_response.text = json.dumps(low_conf_scores)
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

def test_extract_low_confidence_vague_input():
    """Vague input should return low_confidence status."""
    with patch("src.engine.engine._get_client", return_value=make_mock_client_low_confidence()):
        result = extract_vark_scores("I like stuff.")
    assert result["status"] == "low_confidence"
    assert "confidence" in result

def test_extract_confidence_score_present():
    """Successful extraction should include a confidence score."""
    with patch("src.engine.engine._get_client", return_value=make_mock_model()):
        result = extract_vark_scores("I love watching videos and drawing diagrams.")
    assert result["status"] == "success"
    assert "confidence" in result
    assert 0 <= result["confidence"] <= 100

def test_process_quiz_low_confidence_does_not_save():
    """Low confidence result should not call save_quiz_progress."""
    with patch("src.engine.engine._get_client", return_value=make_mock_client_low_confidence()):
        with patch("src.engine.engine.save_quiz_progress") as mock_save:
            result = process_quiz_input("session_conf_001", "I like stuff.")
    assert result["status"] == "low_confidence"
    mock_save.assert_not_called()

# --- Post-Results Q&A Tests ---

def test_answer_followup_returns_string():
    """answer_followup should return a non-empty string response."""
    with patch("src.engine.engine._get_client", return_value=make_mock_model()):
        result = answer_followup(
            question="How should I study for math exams?",
            dominant="Visual",
            scores={"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20}
        )
    assert isinstance(result, str)
    assert len(result) > 0

def test_answer_followup_empty_question():
    """Empty question should return a fallback string."""
    result = answer_followup(
        question="",
        dominant="Visual",
        scores={"visual": 55, "auditory": 10, "reading": 15, "kinesthetic": 20}
    )
    assert isinstance(result, str)
    assert len(result) > 0