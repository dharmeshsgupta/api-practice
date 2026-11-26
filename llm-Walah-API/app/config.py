import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"
GEMINI_MODEL = "gemini-3.5-flash-lite"   # or "gemini-3.6-flash"
TIMEOUT = 30  # seconds

