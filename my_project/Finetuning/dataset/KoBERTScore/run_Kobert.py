import json
import sys

sys.path.append("/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/dataset/KoBERTScore")

from KoBERTScore.score import BERTScore

model_name = "beomi/kcbert-base"
bertscore = BERTScore(model_name, best_layer=4)

MODEL_NAME = "beomi/kcbert-base"
dataset_name = "dataset_0615_filtered"
input_jsonl = f"/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/dataset/_dataset/{dataset_name}.jsonl"
output_jsonl = f"/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/dataset/_dataset/{dataset_name}_KBS.jsonl"

data_list = []
candidates = []
references = []

with open(input_jsonl, "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        if "instruct" in dataset_name:
            candidates.append(data["input"])
            references.append(data["output"])
        else: 
            candidates.append(data["content"])
            references.append(data["transformed_content"])
        data_list.append(data)

print(f"✅ 총 {len(data_list)}개 데이터, BERTScore 계산 시작... {dataset_name} 데이터셋")

scores = bertscore(references, candidates, batch_size=128)
# print(scores)

bar_length = 40
for idx, (data, f1) in enumerate(zip(data_list, scores), 1):
    data["kobertscore_f1"] = float(f1)
    if idx % 10 == 0 or idx == len(data_list):
        percent = idx / len(data_list)
        filled_len = int(bar_length * percent)
        bar = "█" * filled_len + "-" * (bar_length - filled_len)
        print(f"\r진행률: |{bar}| {idx}/{len(data_list)} ({percent*100:.1f}%)", end="")
        sys.stdout.flush()

print() 

with open(output_jsonl, "w", encoding="utf-8") as f:
    for data in data_list:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

print(f"✅ 실행이 정상적으로 종료되었습니다.")
print(f"✅ 결과 파일: {output_jsonl}")