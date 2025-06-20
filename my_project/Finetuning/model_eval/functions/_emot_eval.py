import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1. 감정 매핑표
label_map = {
    "normal": "neutral",
    "happy": "joy",
    "sad": "sadness",
    "angry": "anger",
    "grumpy": "disgust",
    "curious": "surprise"
}

# 2. 모델/토크나이저 로드
MODEL_NAME = "beomi/KcELECTRA-base-emotion"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
id2label = model.config.id2label
label2id = model.config.label2id

# 3. 평가 함수 (한 샘플)
def emotion_classify_score(text, gold_emotion):
    # gold_emotion(내 감정) -> 모델 감정으로 변환
    if gold_emotion not in label_map:
        return None  # 평가 불가
    target_label = label_map[gold_emotion]
    if target_label not in label2id:
        return None  # 평가 불가
    
    # inference
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0]
    pred_idx = probs.argmax().item()
    pred_label = id2label[pred_idx]
    target_idx = label2id[target_label]
    target_prob = probs[target_idx].item()
    match = int(pred_label == target_label)
    return {
        "pred_label": pred_label,
        "target_label": target_label,
        "target_prob": float(target_prob),
        "match": match
    }

# 4. 전체 jsonl 파일 평가
def evaluate_jsonl(input_path):
    total, correct, sum_prob = 0, 0, 0.0
    results = []
    with open(input_path, "r", encoding="utf-8") as fin:
        for line in fin:
            data = json.loads(line)
            text = data.get("transformed_content", "")
            gold_emotion = data.get("emotion", "")
            score = emotion_classify_score(text, gold_emotion)
            if score is not None:
                total += 1
                correct += score["match"]
                sum_prob += score["target_prob"]
                # 결과 기록(필요시)
                results.append({
                    **data,
                    "pred_label": score["pred_label"],
                    "target_label": score["target_label"],
                    "target_prob": score["target_prob"],
                    "emotion_match": score["match"]
                })
    if total == 0:
        print("평가 가능한 샘플이 없습니다.")
        return
    acc = correct / total
    avg_prob = sum_prob / total
    print(f"전체 샘플: {total}")
    print(f"감정 일치 Accuracy: {acc:.3f}")
    print(f"평균 target 감정 확률: {avg_prob:.3f}")
    # 필요시 결과 반환
    return results

# 5. 사용 예시
if __name__ == "__main__":
    input_path = "your_dataset.jsonl"
    evaluate_jsonl(input_path)
