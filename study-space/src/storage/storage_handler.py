"""
src/storage/storage_handler.py

In-memory storage handler for the Study Space quiz application.
"""

# Module-level dictionary to track saved sessions
SESSION_STORE = {}

def save_quiz_progress(session_id: str, scores: dict) -> dict:
    """
    Saves the user's quiz progress to the local SESSION_STORE.
    
    Args:
        session_id (str): Unique identifier for the quiz session.
        scores (dict): Dictionary containing "visual", "auditory", 
                       "reading", and "kinesthetic" scores.
                       
    Returns:
        dict: Status message indicating success, exists, or error.
    """
    required_keys = {"visual", "auditory", "reading", "kinesthetic"}
    
    # 1. Validate required score keys
    if not all(key in scores for key in required_keys):
        return {
            "status": "error", 
            "message": "Missing required score fields."
        }
    
    # 2. Check if session_id already exists
    if session_id in SESSION_STORE:
        return {
            "status": "exists", 
            "message": "Session already recorded."
        }
    
    # 3. Save to in-memory storage
    SESSION_STORE[session_id] = scores
    
    return {
        "status": "success", 
        "id": session_id
    }