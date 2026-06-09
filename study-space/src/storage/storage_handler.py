import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from dotenv import load_dotenv
import os
import json
from datetime import datetime

REQUIRED_KEYS = ["visual", "auditory", "reading", "kinesthetic"]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

load_dotenv()


def _get_credentials():
    """Load credentials from file or environment variable."""
    # Try environment variable first (Railway)
    creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    if creds_json:
        creds_dict = json.loads(creds_json)
        return service_account.Credentials.from_service_account_info(
            creds_dict, scopes=SCOPES
        )

    # Fall back to file (local)
    service_path = os.environ.get("SERVICE_ACCOUNT_FILE", "service_account.json")
    if os.path.exists(service_path):
        return Credentials.from_service_account_file(service_path, scopes=SCOPES)

    return None


def _get_sheet():
    creds = _get_credentials()
    if creds is None:
        raise Exception("No credentials found. Set GOOGLE_APPLICATION_CREDENTIALS_JSON or provide service_account.json.")
    client = gspread.authorize(creds)
    sheet_name = os.environ.get("GOOGLE_SHEET_NAME", "StudySpaceResults")
    ss = client.open(sheet_name)
    sheet = ss.sheet1
    return ss, sheet


def save_quiz_progress(session_id: str, scores: dict) -> dict:
    # Validate required keys
    for key in REQUIRED_KEYS:
        if key not in scores:
            return {"status": "error", "message": "Missing required score fields."}

    try:
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
        return {
            "status": "success",
            "id": session_id,
            "saved": True,
            "spreadsheet_title": getattr(ss, 'title', None),
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}