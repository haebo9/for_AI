# #!/bin/bash

# # (선택) 필요한 패키지 설치
# # pip install -r requirements.txt

# # 평가할 데이터셋 이름 지정
# # DATASET_NAME="dataset_0618_filtered"
# DATASET_NAME="test_short"
# MODE="data"  # 또는 model

# # # 평가할 데이터셋 이름 지정
# # DATASET_NAME="test"
# # MODE="model" 

# if [[ "$MODE" == data ]]; then
#     # KoBERTScore 계산 (데이터만)
#     python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/KoBERTScore/run_Kobert.py --dataset "$DATASET_NAME"
#     # 평가 스크립트 실행 (kobert만, LLM 평가 X)
#     python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/run_eval.py --dataset "$DATASET_NAME" --general False --llm False
# fi

# if [[ "$MODE" == model ]]; then
#     # KoBERTScore 계산 (일반화)
#     python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/KoBERTScore/run_Kobert.py --dataset "$DATASET_NAME"
#     python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/KoBERTScore/run_Kobert.py --dataset "${DATASET_NAME}_general"
#     # 평가 스크립트 실행 (도메인+일반화, LLM 평가 O)
#     python /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/run_eval.py --dataset "$DATASET_NAME" --general True --llm True
# fi

# # 사용 예시:
# # sh /Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval/run_eval.sh