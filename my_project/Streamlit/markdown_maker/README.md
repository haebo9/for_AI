---
title: HF Streamlit
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: docker
pinned: false
short_description: 스트림릿으로 구현하는 나의 앱
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# 마크다운 변환기

## 소개
일반 텍스트를 깔끔한 마크다운(README.md용)으로 변환해주는 웹앱입니다.  
OpenAI 또는 Google Gemini API를 활용하여 입력한 텍스트를 자동으로 구조화된 마크다운으로 변환합니다.

---

## 디렉토리 구조
```
markdown_maker/
├── src/
│   ├── app.py        # Streamlit 메인 앱
│   ├── model.py      # 변환 엔진별 마크다운 변환 함수
│   └── config.py     # 환경변수 로드
├── requirements.txt   # 의존성 목록
├── Dockerfile         # 도커 빌드 파일
├── install.sh         # 로컬 설치/초기화 스크립트
├── .dockerignore
├── .gitignore
└── README.md
```
---

## 실행 방법

### 1. 환경 변수 준비
`.env` 파일에 아래와 같이 API 키를 입력하세요.
```
OPENAI_API_KEY=sk-xxxxxx
GEMINI_API_KEY=your-gemini-key
```
- 두 키 중 하나만 있어도 동작합니다.

---

### 2. 로컬 실행
다음 명령어를 입력하여 실행합니다.
```bash
cd markdown_maker
bash install.sh
streamlit run src/app.py
```
- 기본 접속: [http://localhost:8501](http://localhost:8501)

---

### 3. Docker로 실행

#### 빌드
```bash
docker build -t my-streamlit-app .
```

#### 실행
```bash
docker run -p 7860:7860 --env-file .env my-streamlit-app
```
- 접속: [http://localhost:7860](http://localhost:7860)

---

## 주요 기능

- **비밀번호 인증**: 4자리 숫자 입력 필요(기본값: 9999, `src/app.py`에서 변경 가능)
- **변환 엔진 선택**: OpenAI 또는 Gemini 중 선택
- **마크다운 변환**: 입력 텍스트를 README용 마크다운으로 변환
- **코드/미리보기 탭**: 변환 결과를 코드로 복사하거나, 실시간 미리보기 가능
- **API 키 보안**: .env 파일 또는 환경변수로 관리

---

## 제작자

- [haebo9 github](https://github.com/haebo9/for_AI)
