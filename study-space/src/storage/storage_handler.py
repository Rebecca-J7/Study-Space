import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

REQUIRED_KEYS = ["visual", "auditory", "reading", "kinesthetic"]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def _get_sheet():
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open("StudySpaceResults").sheet1

def save_quiz_progress(session_id: str, scores: dict) -> dict:
    # Validate required keys
    for key in REQUIRED_KEYS:
        if key not in scores:
            return {"status": "error", "message": "Missing required score fields."}

    try:
        sheet = _get_sheet()
        existing = sheet.col_values(1)  # all session_ids in column 1

        # Duplicate check
        if session_id in existing:
            return {"status": "exists", "message": "Session already recorded."}

        # Append new row
        row = [
            session_id,
            scores["visual"],
            scores["auditory"],
            scores["reading"],
            scores["kinesthetic"],
            datetime.now().isoformat()
        ]
        sheet.append_row(row)
        return {"status": "success", "id": session_id}

    except Exception as e:
        return {"status": "error", "message": str(e)}