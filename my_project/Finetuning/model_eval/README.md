## 성능 평가 기준
### 도메인 성능 테스트

> **동물 유형 (post_type)**
  - cat (고양이)
  - dog (강아지)

> **감정 (emotion)**
  - normal (일반)
  - joy (기쁨)
  - sadness (슬픔)
  - anger (분노)
  - surprise (놀람)
  - fear (공포)
  - disgust (혐오)

---

### 일반화 테스트 

> 신규 동물 (6종):
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

### 2. 평가 방법

1. **KoBERTScore 산출**
   - `run_Kobert.py`를 실행하여 각 데이터셋(`test`, `test_general` 등)에 대해 KoBERTScore를 계산하고 결과 파일(`_kbs.jsonl`)을 생성합니다.

2. **LLM 평가 및 통합 평가**
   - `run_eval.py`를 실행하여 KoBERTScore와 LLM 평가(의미 보존, 스타일 일치, 자연스러움, 형식 적합성)를 함께 평가합니다.
   - 결과는 샘플별 CSV와 통계 요약으로 저장됩니다.

3. **통계 및 결과 확인**
   - 전체 평균, 감정별/동물별 평균, 0.5 이하 KoBERTScore 비율, LLM 평가 기준별 평균 점수를 확인할 수 있습니다.
