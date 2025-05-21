from fastapi import FastAPI, Request, Query, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from model_sql_chat import ChatModel
from model_translate import TranslateModel
import logging
import json


# 앱/모델 인스턴스 설정 
app = FastAPI() 
chat_model = ChatModel()
translate_model = TranslateModel()

################ ChatModel ##################
# ChatModel API 
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat")
async def chat(message: str, session_id: str = "default_session"):
    response = await chat_model.chat(message, session_id)
    return {"response": response}

################ TranslateModel API ##################

@app.get("/translates")
async def translates(
    text: str = Query(None, description="번역할 텍스트"),
    language: str = Query("en", description="번역할 언어"),
    session_id: str = Query("default_thread", description="세션 ID")
):
    top_languages = {
        "en": "영어 (English)",
        "ko": "한국어 (Korean)",
        "ja": "일본어 (Japanese)",
        "zh": "중국어 (Chinese)",
        "es": "스페인어 (Spanish)",
        "fr": "프랑스어 (French)",
        "de": "독일어 (German)",
        "ru": "러시아어 (Russian)",
        "ar": "아랍어 (Arabic)",
        "pt": "포르투갈어 (Portuguese)"
    }
    if text is None:
        return Response(
            content=json.dumps(
                {
                    "message": "번역을 원하시는 텍스트를 입력해주세요.",
                    "usage": "/translates?text=<번역할 텍스트>&language=<번역할 언어>&session_id=<세션 ID>",
                    "available_languages": top_languages,
                },
                ensure_ascii=False,
                indent=4,
            ),
            media_type="application/json",
        )

    try:
        response = await translate_model.translate(text, language, session_id)
        return Response(
            content=json.dumps(
                {"original_text": text, 
                 "translated_text": response, 
                 "target_language": language}, 
                 ensure_ascii=False,indent=4), 
                 media_type="application/json")
    except Exception as e:
        logging.error(f"Error in /translates: {e}")
        return Response(
            content=json.dumps(
                {"error": str(e)}, 
                ensure_ascii=False, 
                indent=4), 
                media_type="application/json")