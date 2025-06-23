## 성능 평가
### 평가 기준

> **KoBERTScore**  
  - 원문과 변환문장의 의미 유사도를 BERT 기반 임베딩으로 정량 평가  
  - F1 점수(0~1, 높을수록 의미 보존이 잘 됨)

> **LLM 평가**  
  - OpenAI GPT 기반으로 아래 4가지 항목을 1~5점(0~1로 정규화)으로 평가  
    1. **의미 보존**: 원문의 핵심 의미가 잘 유지되었는가  
    2. **스타일 일치**: 감정/동물 유형의 말투, 어휘, 이모지 등이 잘 반영되었는가  
    3. **자연스러움**: 한국어로서 어색하지 않고 자연스러운가  
    4. **형식 적합성**: 요구 형식(문장부호, 이모지, 길이 등)이 잘 지켜졌는가  
  - 각 항목 점수의 평균을 LLM 평가 점수로 사용

> **최종 점수**  
  - KoBERTScore와 LLM 평가 점수를 0.5:0.5로 가중 평균

---
### 도메인 성능 테스트

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

### 일반화 테스트 

> 신규 동물 (6종):
> 다른 동물과 감정에 대해서도 말투 변환이 가능한지 ?
- hamster (햄스터)
- rabbit (토끼)
- tiger (호랑이)
- parrot (앵무새)
- turtle (거북이)
- bear (곰)

> 신규 감정 (6종):
- excited (신남/흥분)
- proud (자랑스러움/으쓱함)
- shy (수줍음/부끄러움)
- confused (혼란스러움/어리둥절)
- jealous (질투)
- sleepy (졸림)

---

### 평가 방법

1. **KoBERTScore 산출**
   - `run_Kobert.py`를 실행하여 각 데이터셋(`test`, `test_general` 등)에 대해 KoBERTScore를 계산하고 결과 파일(`_kbs.jsonl`)을 생성합니다.

2. **LLM 평가 및 통합 평가**
   - `run_eval.py`를 실행하여 KoBERTScore와 LLM 평가(의미 보존, 스타일 일치, 자연스러움, 형식 적합성)를 함께 평가합니다.
   - 결과는 샘플별 CSV와 통계 요약으로 저장됩니다.

3. **통계 및 결과 확인**
   - 전체 평균, 감정별/동물별 평균, 0.5 이하 KoBERTScore 비율, LLM 평가 기준별 평균 점수를 확인할 수 있습니다.

## 파일 구조 
```
model_eval/
├─ run_eval.py # 평가 메인 스크립트
├─ run_eval.sh # 평가 자동화 bash 스크립트
├─ functions.py # 평가/통계 함수
├─ input_only.py # LLM 입력용 jsonl 생성
├─ requirements.txt # 필요 패키지 목록
├─ jsonl/ # 입력/변환/KoBERTScore 결과 데이터
├─ csv/ # 평가 결과 CSV
├─ input/ # LLM 입력용 jsonl
└─ README.md # 설명서
```

## 참고
- OpenAI API 키 필요: `.env`에 `OPENAI_KEY` 등록
- 패키지 설치: `pip install -r requirements.txt`