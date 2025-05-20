import openai
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Check if the API key is available
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is not set. Please check your .env file.")

# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY

# Define a prompt template using Langchain with Korean instructions
prompt_template = PromptTemplate(
    input_variables=["text"],
    template=(
        "당신은 일반 텍스트를 GitHub README.md 파일에 적합한 잘 형식화된 마크다운으로 변환하는 "
        "도움이 되는 어시스턴트입니다. 출력이 명확하고 간결하며 적절한 마크다운 구문을 사용하도록 하세요."
        "필요하다면 문장의 구조나 형식으로 모두 변경하여 글을 작성하시오."
        "그리고 코드 블록을 만들어서 코드를 작성하시오."
        "답변은 한국어로 작성하시오."
        "다음은 마크다운으로 변환해야 할 텍스트입니다:\n\n{text}"
    )
)

def convert_to_markdown(text):
    try:
        # Use the prompt template to format the input
        prompt = prompt_template.format(text=text)
        
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt}
            ]
        )
        # Return the content without wrapping it in backticks
        markdown_content = response.choices[0].message['content'].strip()
        return markdown_content
    except Exception as e:
        # Log the error or handle it as needed
        return f"An error occurred: {str(e)}"