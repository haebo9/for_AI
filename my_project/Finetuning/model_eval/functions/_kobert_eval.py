from KoBERTScore.score import BERTScore
from transformers import AutoTokenizer
import json
import os

class KobertEvaluator:
    def __init__(self, model_name: str = "beomi/kcbert-base", best_layer: int = 4, max_tokens: int = 290):
        if not isinstance(best_layer, int):
            raise ValueError("best_layer는 반드시 int여야 합니다.")
        self.bertscore = BERTScore(model_name, best_layer=best_layer)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_tokens = max_tokens

    def truncate_text(self, text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        input_ids = self.tokenizer.encode(text, add_special_tokens=False)
        if len(input_ids) > self.max_tokens:
            input_ids = input_ids[:self.max_tokens]
        return self.tokenizer.decode(input_ids, skip_special_tokens=True)


    def evaluate(self, input_path: str, batch_size: int = 128) -> list:
        results = []
        data_list = []
        candidates = []
        references = []
        bar_length = 40

        filename = os.path.basename(input_path)
        is_instruct = "instruct" in filename

        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                if is_instruct:
                    src = self.truncate_text(data.get("input", ""))
                    hyp = self.truncate_text(data.get("output", ""))
                else:
                    src = self.truncate_text(data.get("content", ""))
                    hyp = self.truncate_text(data.get("transformed_content", ""))
                candidates.append(hyp)      # hyp가 candidate
                references.append(src)      # src가 reference
                data_list.append(data)

        print(f"⭕ 총 {len(data_list)}개 데이터, BERTScore 계산 시작...")
        print(f"-> 데이터셋 : {filename}")

        # print(f"references type: {type(references)}, candidates type: {type(candidates)}")
        # print(f"references sample: {references[:2]}")
        # print(f"candidates sample: {candidates[:2]}")

        scores = self.bertscore(references, candidates, batch_size=batch_size)
        if isinstance(scores, tuple) and len(scores) == 3:
            _, _, scores = scores  # F1만 사용

        for idx, (data, f1) in enumerate(zip(data_list, scores), 1):
            data["kobertscore_f1"] = round(float(f1), 5)
            results.append(data)
            percent = idx / len(data_list)
            filled_len = int(bar_length * percent)
            bar = "|" * filled_len + "-" * (bar_length - filled_len)
            print(f"\r진행률: |{bar}| {idx}/{len(data_list)} ({percent*100:.1f}%)", end="", flush=True)
        print()
        return results

    def evaluate_from_data(self, data_list: list) -> list:
        candidates = []
        references = []
        for item in data_list:
            candidates.append(self.truncate_text(item.get("transformed_content", "")))
            references.append(self.truncate_text(item.get("content", "")))
        scores = self.bertscore(references, candidates, batch_size=len(data_list))
        if isinstance(scores, tuple) and len(scores) == 3:
            _, _, scores = scores  # F1만 사용
        results = []
        for i, item in enumerate(data_list):
            k_score = float(scores[i]) if i < len(scores) else 0.0
            item["kobertscore_f1"] = round(k_score, 5)
            results.append(item)
        return results