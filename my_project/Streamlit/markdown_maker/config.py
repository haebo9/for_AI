import os
from dotenv import load_dotenv

# Hugging Face Space에서는 secrets가 환경변수로 자동 주입됨
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# (선택) 로컬 개발 환경에서 .env 사용
if OPENAI_API_KEY is None or GEMINI_API_KEY is None:
    load_dotenv()
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")