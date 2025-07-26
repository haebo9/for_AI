from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import SQLChatMessageHistory
from fastapi import FastAPI
import logging

# Load environment variables
load_dotenv()

app = FastAPI()

class TranslateModel:
    def __init__(self, model_name="gpt-4o-mini", model_provider="openai"):
        # Initialize the model for LangChain
        self.model = init_chat_model(model_name, model_provider=model_provider)

        # Set up the prompt for LangChain
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. Translate the given text into {language}."),
                ("human", "{text}"),
            ]
        )

        # Set up SQLite-based chat message history
        self.chat_message_history = SQLChatMessageHistory(
            session_id="test_session_id", connection="sqlite:///sqlite.db"
        )

    async def translate(self, text: str, language: str = "en", session_id: str = "default_thread"):
        """Translates the user's input using the model with a translation prompt."""
        try:
            self.chat_message_history = SQLChatMessageHistory(session_id=session_id, connection="sqlite:///sqlite.db")
            human_message = HumanMessage(content=text)
            self.chat_message_history.add_message(human_message)

            prompt = self.prompt_template.invoke({"language": language, "text": text})
            response = await self.model.ainvoke(prompt)

            self.chat_message_history.add_message(response)
            return response.content
        except Exception as e:
            logging.error(f"Error in translate: {e}")
            raise e

translate_model = TranslateModel()

@app.get("/translates")
async def translates(text: str, language: str = "en", session_id: str = "default_thread"):
    try:
        response = await translate_model.translate(text, language, session_id)
        return {"original_text": text, "translated_text": response, "target_language": language}
    except Exception as e:
        logging.error(f"Error in /translates: {e}")
        return {"error": str(e)}