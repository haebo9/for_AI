# 성능 평가

---
## 도메인 성능 테스트

> **동물 유형 (post_type)**
  - cat (고양이)
  - dog (강아지)

> **감정 (emotion)**
  - normal (일반)
  - happy (기쁨)
  - sad (슬픔)
  - angry (분노)
  - grumpy (까칠)
  - curious (호기심)

---

## 주요 스크립트 설명

- **run_eval.py**  
  다양한 평가 기준(KoBERTScore, LLM, BLEU, Perplexity 등)을 한 번에 실행하고 결과를 jsonl로 저장합니다.
- **run_eval.sh**  
  여러 데이터셋에 대해 반복적으로 평가를 자동화합니다.
- **input_only.py**  
  평가 입력용 jsonl 파일을 생성합니다.
- **functions/**  
- **functions/**  
  - `_kobert_eval.py`:  
    KoBERTScore를 사용하여 원문과 변환문장의 의미 유사도를 BERT 임베딩 기반으로 정량 평가(F1 점수 산출).
  - `_type_eval.py`:  
    변환문장의 어미, 말투, 스타일이 요구 조건(동물/감정별 말투 등)에 맞게 반영되었는지 규칙 기반으로 평가.
  - `_quality_eval.py`:  
    OpenAI GPT 등 LLM을 활용해 의미 보존, 스타일 일치, 자연스러움, 형식 적합성 등 항목별로 변환문장 품질을 평가.
  - `_bleu_eval.py`:  
    BLEU 점수를 계산하여 원문과 변환문장 간 n-gram 기반 유사도를 평가(기계번역 품질 지표).
  - `_perplex_eval.py`:  
    KoGPT2 등 언어모델을 활용해 변환문장의 Perplexity(문장 자연스러움)를 평가, 낮을수록 자연스러움.
  - `main_eval.py`:  
    개별 평가 모듈을 통합 실행, 여러 기준의 결과를 종합/통계 처리하고 jsonl로 저장.
  - `visualize.py`:  
    평가 결과(jsonl 등)를 시각화하여 점수 분포, 항목별 비교, 이상치 탐지 등 분석 지원.

- **KoBERTScore/**  
  KoBERTScore 관련 코드, 실험, 리소스, 테스트 등 포함

---

## 실행 방법

1. **의존성 설치**
   ```bash
   export PYTHONPATH=$PYTHONPATH:/Users/seo/Documents/_code/for_AI/my_project/Finetuning/model_eval/KoBERTScore
   pip install -r requirements.txt
   ```

2. **OpenAI API 키 등록**
   - `.env` 파일에 `OPENAI_KEY=your-key` 추가

3. **평가 실행**
   ```bash
   python run_eval.py
   ```
   또는
   ```bash
   bash run_eval.sh
   ```

4. **결과 확인**
   - `_output/` 폴더에 평가 결과(jsonl) 생성
   - 평균 점수, 항목별 통계 등 확인 가능

---

## 참고

- 입력/출력 데이터 포맷, 상세 옵션 등은 각 스크립트 상단 주석 및 예시 파일 참고
- 평가 기준 및 방식은 필요에 따라 커스터마이즈 가능

---

문의: 담당자에게 연락 또는 이슈 등록