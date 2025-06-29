from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import math
import json
from typing import List, Dict, Optional

class PerplexityEvaluator:
    def __init__(self, model_name: str):
        self.device = "cpu"
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.to(self.device)
        if self.tokenizer.pad_token is None:
            self.tokenizer.add_special_tokens({'pad_token': '[PAD]'})
            self.model.resize_token_embeddings(len(self.tokenizer))

    def calculate_perplexity_batch(self, texts: List[str], max_length: int = 300) -> List[Optional[float]]:
        valid_texts = [t if t.strip() else self.tokenizer.pad_token for t in texts]
        inputs = self.tokenizer(
            valid_texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs, labels=inputs["input_ids"])
            shift_logits = outputs.logits[..., :-1, :].contiguous()
            shift_labels = inputs["input_ids"][..., 1:].contiguous()
            loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
            loss = loss_fct(
                shift_logits.view(-1, shift_logits.size(-1)),
                shift_labels.view(-1)
            ).view(shift_labels.size())
            mask = (shift_labels != self.tokenizer.pad_token_id)
            sum_loss = (loss * mask).sum(dim=1)
            count = mask.sum(dim=1)
            mean_loss = [s.item() / c.item() if c.item() > 0 else None for s, c in zip(sum_loss, count)]
            perplexities = [math.exp(l) if l is not None else None for l in mean_loss]
        return perplexities
    
def add_perplexity_score_to_jsonl(
    self,
    input_jsonl_path: str,
    output_jsonl_path: str,
    text_key: str = "transformed_content",
    batch_size: int = 8,
    max_length: int = 300,
    thres_perplexity_score: float = 0.05
) -> int:
    texts: List[str] = []
    datas: List[Dict] = []

    with open(input_jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            text = data.get(text_key, "")
            texts.append(text)
            datas.append(data)     

    # bad_count = 0
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_ppls = self.calculate_perplexity_batch(batch_texts, max_length=max_length)
        for j, ppl in enumerate(batch_ppls):
            datas[i+j]["perplexity_score"] = ppl if ppl is not None else None

    with open(output_jsonl_path, "w", encoding="utf-8") as f:
        for data in datas:
            data.pop("perplexity", None)
            f.write(json.dumps(data, ensure_ascii=False) + "\n")

    # print(f"perplexity_score < {thres_perplexity_score} 인 데이터 개수: {bad_count}개 / {len(datas)}개")
    # return bad_count

if __name__ == "__main__":
    model_name = "skt/kogpt2-base-v2"
    input_jsonl_path = "/Users/seo/Documents/_code/for_AI/my_project/Finetuning/dataset/_dataset/_test/test_short.jsonl"
    output_jsonl_path = "/Users/seo/Documents/_code/for_AI/my_project/Finetuning/model_eval/_output/output_perplexity.jsonl"

    evaluator = PerplexityEvaluator(model_name)
    evaluator.evaluate_file(
        input_jsonl_path=input_jsonl_path,
        text_key="transformed_content",
        output_jsonl_path=output_jsonl_path,
        batch_size=8,
        max_length=300
    )