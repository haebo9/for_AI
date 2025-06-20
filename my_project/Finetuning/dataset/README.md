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