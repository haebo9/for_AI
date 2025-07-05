import json

def filter_jsonl_bytes_by_threshold(
    eval_jsonl_bytes_list,
    thresholds: dict
):
    filtered = []
    for eval_bytes in eval_jsonl_bytes_list:
        lines = eval_bytes.decode("utf-8").splitlines()
        for line in lines:
            data = json.loads(line)
            passed = True
            for key, thres in thresholds.items():
                value = data.get(key)
                if value is None or float(value) < thres:
                    passed = False
                    break
            if passed:
                filtered.append(data)
    return filtered