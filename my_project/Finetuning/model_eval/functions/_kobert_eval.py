import json
import collections

def print_kobertscore_stats(
    data_list: list,
    score_key: str = "kobertscore_f1",
    feature_key: str = "emotion",
    threshold: float = 0.5
) -> None:
    all_scores = [float(data.get(score_key, 0.0)) for data in data_list]
    feature_scores = collections.defaultdict(list)
    for data in data_list:
        if callable(feature_key):
            feature = feature_key(data)
        else:
            feature = data.get(feature_key, "None")
        feature_scores[feature].append(float(data.get(score_key, 0.0)))

    print(f"\n📊 {feature_key if isinstance(feature_key, str) else '조합'}별 KoBERTScore 평균")
    for feature, values in feature_scores.items():
        avg = sum(values) / len(values)
        print(f"- {feature}: {avg:.3f} (n={len(values)})")

    low_score_count = sum(s <= threshold for s in all_scores)
    print(f"\nBERTScore F1 ≤ {threshold} 인 샘플 개수: {low_score_count} / {len(all_scores)}")

def load_kobertscore_dict(kbs_path: str) -> dict:
    kbs_dict = {}
    with open(kbs_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            key = (data.get("content", ""), data.get("transformed_content", ""))
            kbs_dict[key] = data.get("kobertscore_f1", 0.0)
    return kbs_dict

def kbs_eval(
    input_path: str,
    kbs_path: str,
    output_csv: str = None,
    batch_size: int = 10
) -> list:
    kbs_dict = load_kobertscore_dict(kbs_path)
    results = []
    bar_length = 40

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        total_samples = len(lines)
        idx = 0
        while idx < total_samples:
            batch = []
            for b in range(batch_size):
                if idx + b >= total_samples:
                    break
                data = json.loads(lines[idx + b])
                src = data.get("content", "")
                hyp = data.get("transformed_content", "")
                emotion = data.get("emotion", "")
                post_type = data.get("post_type", "")
                k_score = kbs_dict.get((src, hyp), 0.0)
                batch.append({
                    "src": src,
                    "hyp": hyp,
                    "emotion": emotion,
                    "post_type": post_type,
                    "k_score": k_score,
                    "raw_data": data
                })

            # 결과 저장
            for b in range(len(batch)):
                k_score = batch[b]["k_score"]
                data = batch[b]["raw_data"]
                results.append({
                    "content": batch[b]["src"],
                    "transformed_content": batch[b]["hyp"],
                    "kobertscore_f1": round(k_score, 3),
                    "emotion": batch[b]["emotion"],
                    "post_type": batch[b]["post_type"],
                })

            idx += batch_size
            percent = min(idx, total_samples) / total_samples
            filled_len = int(bar_length * percent)
            bar = "█" * filled_len + "-" * (bar_length - filled_len)
            print(f"\r진행률: |{bar}| {min(idx, total_samples)}/{total_samples} ({percent*100:.1f}%)", end="", flush=True)
        print()
    return results