"""
src/engine/recommender.py

Recommendation engine logic for the Study Space quiz application.
"""

# Static data for study strategies and tools based on VARK styles
STYLE_DATA = {
    "Visual": {
        "strategies": ["Mind maps", "Color-coded notes", "Diagrams"],
        "tools": ["Canva", "Notion", "YouTube"]
    },
    "Auditory": {
        "strategies": ["Read aloud", "Record lectures", "Group discussion"],
        "tools": ["Spotify podcasts", "Voice Memos", "YouTube"]
    },
    "Reading": {
        "strategies": ["Rewrite notes", "Make lists", "Summarize"],
        "tools": ["Notion", "Google Docs", "Anki"]
    },
    "Kinesthetic": {
        "strategies": ["Hands-on practice", "Flashcards", "Teaching others"],
        "tools": ["Anki", "Quizlet", "Khan Academy"]
    }
}

def get_recommendations(vark_result: dict) -> dict:
    """
    Generates study recommendations based on VARK scores and the dominant style.
    
    Args:
        vark_result (dict): Contains "dominant", "visual", "auditory", 
                            "reading", and "kinesthetic" keys.
                            
    Returns:
        dict: Recommendation data with status "success", "tied", or "error".
    """
    required_keys = {"dominant", "visual", "auditory", "reading", "kinesthetic"}
    
    # 1. Validate required keys
    if not all(key in vark_result for key in required_keys):
        return {
            "status": "error",
            "message": "Could not generate recommendations."
        }
    
    # 2. Handle Tied results
    if vark_result["dominant"] == "Tied":
        scores = {
            "Visual": vark_result["visual"],
            "Auditory": vark_result["auditory"],
            "Reading": vark_result["reading"],
            "Kinesthetic": vark_result["kinesthetic"]
        }
        
        max_score = max(scores.values())
        tied_styles = [style for style, score in scores.items() if score == max_score]
        
        # Aggregate strategies from all tied styles
        combined_strategies = []
        for style in tied_styles:
            combined_strategies.extend(STYLE_DATA[style]["strategies"])
            
        return {
            "status": "tied",
            "data": {
                "tied_styles": tied_styles,
                "strategies": list(set(combined_strategies))  # Unique strategies
            }
        }
    
    # 3. Handle Success (Single Dominant Style)
    dominant_style = vark_result["dominant"]
    
    # Ensure the dominant style exists in our data map (handles casing/mapping)
    if dominant_style in STYLE_DATA:
        return {
            "status": "success",
            "data": {
                "dominant": dominant_style,
                "strategies": STYLE_DATA[dominant_style]["strategies"],
                "tools": STYLE_DATA[dominant_style]["tools"]
            }
        }
    
    # Fallback if dominant style string is unrecognized
    return {
        "status": "error",
        "message": "Could not generate recommendations."
    }