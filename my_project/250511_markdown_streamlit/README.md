# 마크다운 코드 변환기

## 개요

이 프로젝트는 일반 텍스트를 GitHub README.md 파일에 적합한 잘 형식화된 마크다운으로 변환하는 웹 애플리케이션입니다. 사용자의 입력에 따라 출력이 명확하고 간결하게 생성됩니다.

## 파일 구조

- **`main.py`**: 사용자 인터페이스를 위한 Streamlit 애플리케이션 코드.
- **`model.py`**: OpenAI API와 Langchain을 사용하여 변환 로직을 처리하는 코드.
- **`requirements.txt`**: 프로젝트에 필요한 Python 패키지 목록.

## 핵심 설명

이 애플리케이션은 웹 인터페이스를 위해 Streamlit을 사용하며, 텍스트 변환을 위해 OpenAI의 API를 활용합니다. Langchain의 `PromptTemplate`을 이용하여 변환 과정에 필요한 동적 프롬프트를 생성합니다.

## 설치 및 실행

1. **의존성 설치**:
   ```bash
   pip install -r requirements.txt
   ```

2. **환경 설정**:
   `.env` 파일에 OpenAI API 키가 포함되어 있는지 확인하세요:
   ```bash
   OPENAI_API_KEY=your_openai_api_key
   ```

3. **애플리케이션 실행**:
   ```bash
   streamlit run main.py
   ```

## 주요 기능

- **동적 프롬프트 생성**: Langchain을 사용하여 유연한 프롬프트 생성 기능을 제공합니다.
- **안전한 API 키 관리**: `python-dotenv`를 활용하여 환경 변수를 안전하게 관리합니다.

## 프로젝트 파일 구조

```
/project-root
├── main.py            # 사용자 인터페이스를 위한 Streamlit 애플리케이션 코드.
├── model.py           # OpenAI API와 Langchain을 이용한 변환 로직.
├── requirements.txt    # Python 패키지 의존성 목록.
└── README.md           # 프로젝트 개요 및 실행 방법.
```

### 출력 결과
