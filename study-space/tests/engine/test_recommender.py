from src.engine.recommender import get_recommendations

VISUAL_RESULT = {
    "dominant": "Visual",
    "visual": 40,
    "auditory": 20,
    "reading": 15,
    "kinesthetic": 25
}

TIED_RESULT = {
    "dominant": "Tied",
    "visual": 40,
    "auditory": 40,
    "reading": 10,
    "kinesthetic": 10
}

def test_recommendations_success():
    result = get_recommendations(VISUAL_RESULT)
    assert result["status"] == "success"
    assert "dominant" in result["data"]
    assert "strategies" in result["data"]
    assert "tools" in result["data"]

def test_recommendations_tied():
    result = get_recommendations(TIED_RESULT)
    assert result["status"] == "tied"
    assert "tied_styles" in result["data"]

def test_recommendations_missing_input():
    result = get_recommendations({})
    assert result["status"] == "error"