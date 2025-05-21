#!/bin/bash

# 스크립트가 오류 발생 시 중단되도록 설정
set -e

# 가상 환경 디렉토리 이름
VENV_DIR=".venv"

# 가상 환경 생성
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

# 가상 환경 활성화
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# 의존성 설치
echo "Installing dependencies..."
pip install -r requirements.txt

# 환경 변수 설정
ENV_FILE=".env"
echo "Setting up environment variables..."

# .env 파일 생성
if [ ! -f "$ENV_FILE" ]; then
  echo "Creating $ENV_FILE file..."
  touch "$ENV_FILE"
fi

# 함수: 키 추가
add_key() {
  local key_name=$1
  local key_value
  read -p "Enter your $key_name: " key_value
  echo "$key_name=$key_value" >> "$ENV_FILE"
}

# OpenAI API 키 추가
echo "Please enter your OpenAI API key:"
add_key "OPENAI_API_KEY"

echo "Your OpenAI API key has been saved in the $ENV_FILE file."

# Streamlit 애플리케이션 실행
echo "Running Streamlit application..."
streamlit run main.py