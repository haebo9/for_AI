import openai
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from config import OPENAI_API_KEY, GEMINI_API_KEY  # config에서 키 import

# OpenAI API 키 설정
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Gemini API 키 설정
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# 프롬프트 템플릿 (공통)
prompt_template = PromptTemplate(
    input_variables=["text"],
    template=(
        "You are an expert assistant that converts plain text into a well-structured, highly readable Markdown document suitable for a GitHub README.md file. "
        "Your output must be clear, concise, and use proper Markdown syntax. "
        "Actively utilize Markdown features such as headers, lists, tables, and especially code blocks where code is present or implied. "
        "For any code, always use fenced code blocks with the correct language tag (e.g., ```python, ```bash, etc.). "
        "If the text contains instructions, examples, or data, format them using appropriate Markdown elements for maximum clarity. "
        "For file/folder structures, always wrap them in a Markdown code block (using triple backticks: ```), and use tree symbols such as ├──, └──, │, and spaces for indentation to represent the hierarchy clearly. "
        "Restructure or rephrase sentences as needed to improve readability and formatting. "
        "Do not include unnecessary explanations or verbose text—focus on delivering a clean, professional Markdown output. "
        "Respond in Korean. "
        "Here is the text to convert into Markdown:\n\n{text}"
    )
)

def convert_to_markdown(text: str, provider: str = "openai") -> str:
    """
    provider: "openai" 또는 "gemini" 중 선택
    """
    prompt = prompt_template.format(text=text)
    try:
        if provider == "openai":
            if not OPENAI_API_KEY:
                return "OpenAI API 키가 설정되어 있지 않습니다."
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )
            markdown_content = response.choices[0].message['content'].strip()
            return markdown_content

        elif provider == "gemini":
            if not GEMINI_API_KEY:
                return "Gemini API 키가 설정되어 있지 않습니다."
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(prompt)
            return response.text.strip()

        else:
            return "지원하지 않는 provider입니다. (openai 또는 gemini 중 선택)"

    except Exception as e:
        return f"An error occurred: {str(e)}"