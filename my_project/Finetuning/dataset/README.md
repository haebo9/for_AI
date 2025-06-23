<<<<<<< HEAD
# 평가 모델 개발
## 데이터셋 
> dataset_0515_made.jsonl : 초기 유저 데이터
```
📊 KoBERTScore
⭐ 전체 평균: 0.658
- 감정별 평균:
  - happy: 0.639 (n=198)
  - sad: 0.665 (n=12)
  - grumpy: 0.670 (n=14)
  - angry: 0.654 (n=11)
  - curious: 0.618 (n=21)
  - normal: 0.709 (n=86)
- 0.5 이하 비율: 6.4% (22/342)

==== dataset_0515_made.jsonl ====
✅ 필터링 완료 및 새로운 파일 생성 완료
! 변환 전 데이터 개수: 342
! 변환 후 데이터 개수: 263

--- dog : 총 49개 ---
normal: 19
happy: 4
sad: 6
grumpy: 8
angry: 4
curious: 8

--- cat : 총 214개 ---
normal: 57
happy: 125
sad: 6
grumpy: 6
angry: 7
curious: 13
```

> dataset_0527_made.jsonl : 0515 + 감정별/동물별 증폭 데이터
```
📊 KoBERTScore
⭐ 전체 평균: 0.635
- 감정별 평균:
  - happy: 0.652 (n=290)
  - sad: 0.600 (n=125)
  - grumpy: 0.626 (n=134)
  - angry: 0.607 (n=142)
  - curious: 0.575 (n=116)
  - normal: 0.680 (n=256)
- 0.5 이하 비율: 5.1% (54/1063)

==== dataset_0527_made.jsonl ====
✅ 필터링 완료 및 새로운 파일 생성 완료
! 변환 전 데이터 개수: 1063
! 변환 후 데이터 개수: 1033

--- dog : 총 442개 ---
normal: 109
happy: 92
sad: 55
grumpy: 59
angry: 72
curious: 55

--- cat : 총 591개 ---
normal: 133
happy: 192
sad: 69
grumpy: 68
angry: 69
curious: 60
```

> dataset_0615_made.jsonl : 0527 + 추가 유저 데이터 증폭 + 댓글 간단한 변환(cat) 데이터
```
📊 KoBERTScore
⭐ 전체 평균: 0.658
- 감정별 평균:
  - happy: 0.622 (n=675)
  - normal: 0.782 (n=1384)
  - grumpy: 0.584 (n=625)
  - angry: 0.597 (n=636)
  - curious: 0.584 (n=614)
  - sad: 0.632 (n=618)
- 0.5 이하 비율: 7.9% (360/4552)

==== dataset_0615_made.jsonl ====
✅ 필터링 완료 및 새로운 파일 생성 완료
! 변환 전 데이터 개수: 4552
! 변환 후 데이터 개수: 4187

--- cat : 총 2313개 ---
normal: 774
happy: 325
sad: 306
grumpy: 302
angry: 307
curious: 299

--- dog : 총 1874개 ---
normal: 346
happy: 332
sad: 297
grumpy: 295
angry: 309
curious: 295
```
> dataset_0617_made.jsonl : google api 합성 인풋에 대한 Gemini 말투 변환
```
📊 KoBERTScore
⭐ 전체 평균: 0.641
- 감정별 평균:
  - happy: 0.620 (n=84)
  - normal: 0.683 (n=84)
  - grumpy: 0.604 (n=83)
  - angry: 0.647 (n=83)
  - curious: 0.635 (n=83)
  - sad: 0.658 (n=83)
- 0.5 이하 비율: 4.8% (24/500)

==== dataset_0617_made.jsonl ====
✅ 필터링 완료 및 새로운 파일 생성 완료
! 변환 전 데이터 개수: 500
! 변환 후 데이터 개수: 500

--- cat : 총 252개 ---
normal: 42
happy: 42
sad: 42
grumpy: 42
angry: 42
curious: 42

--- dog : 총 248개 ---
normal: 42
happy: 42
sad: 41
grumpy: 41
angry: 41
curious: 41
```

> dataset_0618_made.jsonl : google api 합성 인풋에 대한 Gemini 말투 변환
```
📊 KoBERTScore
⭐ 전체 평균: 0.653
- 감정별 평균:
  - happy: 0.640 (n=664)
  - normal: 0.692 (n=662)
  - grumpy: 0.613 (n=666)
  - angry: 0.648 (n=665)
  - curious: 0.654 (n=660)
  - sad: 0.669 (n=661)
- 0.5 이하 비율: 3.1% (124/3978)

==== dataset_0618_made.jsonl ====
✅ 필터링 완료 및 새로운 파일 생성 완료
! 변환 전 데이터 개수: 3978
! 변환 후 데이터 개수: 3978

--- cat : 총 1989개 ---
normal: 332
happy: 331
sad: 329
grumpy: 333
angry: 332
curious: 332

--- dog : 총 1989개 ---
normal: 330
happy: 333
sad: 332
grumpy: 333
angry: 333
curious: 328
```

> dataset_0619_made.json : google api 합성 인풋에 대한 Gemini 말투 변환 최종 8000개
```
📊 KoBERTScore
⭐ 전체 평균: 0.657
- 감정별 평균:
  - happy: 0.643 (n=1474)
  - normal: 0.697 (n=1468)
  - grumpy: 0.616 (n=1473)
  - angry: 0.651 (n=1475)
  - curious: 0.658 (n=1466)
  - sad: 0.675 (n=1465)
- 0.5 이하 비율: 3.0% (266/8821)

✅ 필터링 완료 및 새로운 파일 생성 완료
! 변환 전 데이터 개수: 8821
! 변환 후 데이터 개수: 8778

--- cat : 총 4394개 ---
normal: 731
happy: 733
sad: 729
grumpy: 734
angry: 735
curious: 732

--- dog : 총 4384개 ---
normal: 730
happy: 733
sad: 730
grumpy: 732
angry: 730
curious: 729
```

> dataset_0619_made.json : google api 합성 인풋에 대한 Gemini 말투 변환 최종 1100개
작성해야 함. 

> test_made.json : 테스트용 google ai studio 합성 데이터
```
📊 KoBERTScore
⭐ 전체 평균: 0.557
- 감정별 평균:
  - happy: 0.544 (n=25)
  - sad: 0.525 (n=19)
  - angry: 0.550 (n=13)
  - grumpy: 0.594 (n=13)
  - curious: 0.555 (n=16)
  - normal: 0.600 (n=14)
- 0.5 이하 비율: 23.0% (23/100)
```
=======
# 파인튜닝 데이터셋 전처리 및 변환 도구 (`dataset/`)

이 디렉토리는 파인튜닝용 JSONL 데이터셋의 **정제, 필터링, 컬럼 변환, 후처리**를 위한 스크립트와 샘플 데이터를 포함합니다.

---

## 주요 파일 설명

- **preprocessing.py**  
  데이터셋의 품질을 높이기 위한 필터링, 텍스트 후처리, 중복제거, 통계 출력 등 전체 파이프라인 제공
- **comm_to_post.py**  
  컬럼명 일괄 변경, 컬럼 순서 지정, 라벨 추가 등 데이터 구조 변환 스크립트
- **_dataset/**  
  실제 데이터셋(jsonl) 파일 저장 폴더 (입력/출력/중간 결과 등)
- **data_maker.py**  
  (비어 있음, 추후 데이터 생성용 스크립트 작성 가능)

---

## 데이터 전처리/필터링 기준

### 1. **삭제(완전 제거) 조건**
- `content`, `transformed_content` 모두 없음
- 두 필드 모두 5자 미만이거나 의미 없는 텍스트(특수문자/숫자/공백만)
- 시스템/명령어/SQL/해킹 등 위험 키워드 포함(예: system, drop table, script, 해킹 등)

### 2. **수정(후처리) 조건**
- 해시태그, 이모지 과다/연속, 반복 단어, 비알파벳 시작, 변환 텍스트 과다 길이 등
- 후처리: 해시태그/특수공백/줄바꿈/특수문자/이모지/반복/불필요단어/공백 정리, 5자 미만 오류 메시지 대체, 200자 초과시 자르기 등

### 3. **중복 제거**
- 기본값: `content + emotion + post_type` 세 가지가 모두 같을 때만 중복으로 간주하여 1개만 남김
- 옵션으로 중복 제거를 끌 수도 있음

---

## 사용 방법

### 1. 데이터 전처리 및 필터링
```bash
python preprocessing.py -c [코드] [--skip N]
```
- `-c [코드]` : 데이터셋 파일명 코드 (예: 0615)
- `--skip N` : N번째 줄까지 데이터는 모두 건너뜀(선택)

### 2. 컬럼명/순서/라벨 변환
```bash
python comm_to_post.py
```
- 코드 내에서 입력/출력 파일명, 컬럼명 매핑, 라벨 지정 등 수정 가능

---

## 주요 함수 및 기능 요약

- **TextPostprocessor** : 텍스트 후처리(이모지, 해시태그, 반복, 특수공백, 불필요단어 등)
- **DataFilter** : 삭제/수정 조건 판별(위험키워드, 의미없음, 반복, 해시태그 등)
- **filter_and_postprocess** : 전체 파이프라인(중복제거, 삭제, 후처리, 컬럼정렬)
- **count_features** : post_type별 emotion 분포 통계 출력

---

## 예시

### 입력 데이터 예시
```json
{"content": "#내돈내산 오늘은 고기를 먹었다!", "transformed_content": "🐶🐶🐶🐶🐶 오늘은 정말 맛있는 고기를 먹었다!"}
{"content": "🐾🐾🐾 오늘은 고기를 먹었다!", "transformed_content": "오늘은 정말 맛있는 고기를 먹었다!"}
```

### 필터링 및 후처리 후 데이터 예시
```json
{"post_type": "cat", "emotion": "happy", "content": "오늘은 고기를 먹었다!", "transformed_content": "오늘은 정말 맛있는 고기를 먹었다!"}
```

---

## 참고

- 각 조건별 함수는 독립적으로 구현되어 있어, 필요에 따라 쉽게 수정/확장할 수 있습니다.
- 데이터셋 구조(필드)는 컬럼명 매핑/정렬로 유연하게 변경 가능합니다.
- 통계 출력으로 데이터 분포를 쉽게 확인할 수 있습니다.

---
>>>>>>> 0716fc7 (feat : dataset code)
