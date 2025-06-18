#!/bin/bash

# 2. (선택) 필요한 패키지 설치
# pip install -r requirements.txt

# 평가할 데이터셋 이름 지정
DATASET_NAME="dataset_0617_made"
MODE="data"  # 또는 model

# KoBERTScore 계산 (도메인)
if [[ "$MODE" == data ]]; then
    python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/KoBERTScore/run_Kobert.py --dataset "$DATASET_NAME"
    # 평가 스크립트 실행 (run_eval.py 내부 조건문에 따라 일반화 평가 자동 실행)
    python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/run_eval.py --dataset "$DATASET_NAME" --general False
fi

# KoBERTScore 계산 (일반화)
if [[ "$MODE" == model ]]; then
    python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/KoBERTScore/run_Kobert.py --dataset "${DATASET_NAME}_general"
    python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/run_eval.py --dataset "$DATASET_NAME" --general True
fi