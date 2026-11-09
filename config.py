import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from this project folder, even when the command runs elsewhere.
PROJECT_FOLDER = Path(__file__).resolve().parent
load_dotenv(PROJECT_FOLDER / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite").strip()
GEMINI_FALLBACK_MODELS = os.getenv(
    "GEMINI_FALLBACK_MODELS",
    "gemini-3.7-flash,gemini-3.8-flash"
).strip()

BROWSER_TIMEOUT_MS = 15000
NAVIGATION_TIMEOUT_MS = 30000
