import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
from datetime import datetime

REQUIRED_KEYS = ["visual", "auditory", "reading", "kinesthetic"]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

load_dotenv()


def _get_sheet():
    service_path = os.environ.get("SERVICE_ACCOUNT_FILE", "service_account.json")
    creds = Credentials.from_service_account_file(service_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    ss = client.open("StudySpaceResults")
    sheet = ss.sheet1
    return ss, sheet

def save_quiz_progress(session_id: str, scores: dict) -> dict:
    # Validate required keys
    for key in REQUIRED_KEYS:
        if key not in scores:
            return {"status": "error", "message": "Missing required score fields."}

    try:
        # If service account file is missing, skip saving but return success so UI can continue
        service_path = os.environ.get("SERVICE_ACCOUNT_FILE", "service_account.json")
        if not os.path.exists(service_path):
            return {"status": "success", "id": session_id, "saved": False, "message": "Service account not found; skipping save."}

        ss, sheet = _get_sheet()
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
        info = {
            "status": "success",
            "id": session_id,
            "saved": True,
            "spreadsheet_id": getattr(ss, 'id', None),
            "spreadsheet_title": getattr(ss, 'title', None),
        }
        return info

    except Exception as e:
        return {"status": "error", "message": str(e)}