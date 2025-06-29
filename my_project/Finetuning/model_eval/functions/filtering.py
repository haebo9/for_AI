import json
from functions.visualize import normalize_scores

def filter_jsonl_bytes_by_threshold(
    eval_jsonl_bytes_list,
    thresholds: dict
):
    filtered = []
    for eval_bytes in eval_jsonl_bytes_list:
        lines = eval_bytes.decode("utf-8").splitlines()
        for line in lines:
            data = json.loads(line)
            norm_data = normalize_scores(data)  # 정규화된 점수로 변환
            passed = True
            for key, thres in thresholds.items():
                value = norm_data.get(key)
                if value is None or float(value) < thres:
                    passed = False
                    break
            if passed:
                filtered.append(data)
    return filtered