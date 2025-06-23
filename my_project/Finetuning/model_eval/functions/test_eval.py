import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from KoBERTScore.KoBERTScore.score import BERTScore
from _kobert_eval import KobertEvaluator
from _type_eval import TypeEvaluator
from _llm_eval import LLMEvaluator

if __name__ == "__main__":
    # 샘플 데이터 직접 정의
    test_data = [{
        "content": "나는 오늘 기분이 좋아.",
        "transformed_content": "나는 오늘 기분이 너무 좋아멍!",
        "emotion": "happy",
        "post_type": "dog"
    }]

    # KoBERT 평가 (직접 점수 계산)
    kobert_eval = KobertEvaluator(model_name="beomi/kcbert-base", best_layer=4)
    print("=== KoBERT 평가 ===")
    print(kobert_eval.evaluate_from_data(test_data))

    # 어미 평가
    eomi_eval = TypeEvaluator()
    print("=== 어미 평가 ===")
    print(eomi_eval.evaluate_from_data(test_data))

    # LLM 평가 (OpenAI API 필요)
    llm_eval = LLMEvaluator()
    print("=== LLM 평가 ===")
    print(llm_eval.evaluate_from_data(test_data))
