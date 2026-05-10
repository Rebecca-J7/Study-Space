from src.storage.storage_handler import save_quiz_progress

VALID_SCORES = {
    "visual": 40,
    "auditory": 20,
    "reading": 15,
    "kinesthetic": 25
}

def test_save_success():
    result = save_quiz_progress("session_test_001", VALID_SCORES)
    assert result["status"] == "success"
    assert result["id"] == "session_test_001"

def test_save_duplicate():
    save_quiz_progress("session_dup_001", VALID_SCORES)
    result = save_quiz_progress("session_dup_001", VALID_SCORES)
    assert result["status"] == "exists"

def test_save_missing_fields():
    result = save_quiz_progress("session_bad_001", {"visual": 40})
    assert result["status"] == "error"