import re
import json
import csv

def type_eval(
    input_path: str,
    output_csv: str = None,
    batch_size: int = 10
) -> list:
    # 고양이/강아지 어미 패턴
    cat_endings = ['냥', '냐옹', '이냥', '이다냥', '다먀', '댜옹']
    dog_endings = ['멍', '~다멍', '~냐왈', '~냐멍', '~다왈', '~다개', '~요멍']

    cat_pattern = re.compile("|".join([re.escape(e) for e in cat_endings]))
    dog_pattern = re.compile("|".join([re.escape(e) for e in dog_endings]))

    results = []
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            post_type = data.get("post_type", "")
            transformed = data.get("transformed_content", "")
            wrong_ending = False
            wrong_ending_type = ""
            sample_score = 1  # 기본값: 정상

            if post_type == "dog":
                # 강아지인데 고양이 어미가 들어가면 잘못된 것
                if cat_pattern.search(transformed):
                    wrong_ending = True
                    wrong_ending_type = "cat"
                    sample_score = 0
            elif post_type == "cat":
                # 고양이인데 강아지 어미가 들어가면 잘못된 것
                if dog_pattern.search(transformed):
                    wrong_ending = True
                    wrong_ending_type = "dog"
                    sample_score = 0

            results.append({
                "content": data.get("content", ""),
                "transformed_content": transformed,
                "post_type": post_type,
                "wrong_ending": wrong_ending,
                "wrong_ending_type": wrong_ending_type,
                "sample_score": sample_score
            })

    # 통계 및 점수 출력
    total = len(results)
    wrong = sum(1 for r in results if r["wrong_ending"])
    score = 1 - (wrong / total) if total > 0 else 0.0
    print(f"전체 샘플 수: {total}")
    print(f"잘못된 어미 사용 샘플 수: {wrong} ({wrong/total*100:.1f}%)")
    print(f"어미 적합성 점수: {score:.3f}")

    # csv 저장
    if output_csv:
        with open(output_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    return results