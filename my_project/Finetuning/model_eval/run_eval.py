import argparse
import functions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--general", type=lambda x: x.lower() == "true", default=False, help="일반화 평가도 함께 실행 (True/False)")
    args = parser.parse_args()
    root_path = "/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning/model_eval"

    # 말투 변환 성능 평가
    functions.evaluate_100_dataset(
        f"{root_path}/_jsonl/{args.dataset}.jsonl",
        f"{root_path}/_jsonl/{args.dataset}_kbs.jsonl",
        f"{root_path}/_csv/{args.dataset}.csv",
    )

    # 일반화 성능 평가는 --general 옵션이 True일 때만 실행
    if args.general:
        functions.evaluate_100_dataset(
            f"{root_path}/_jsonl/{args.dataset}_general.jsonl",
            f"{root_path}/_jsonl/{args.dataset}_general_kbs.jsonl",
            f"{root_path}/_csv/{args.dataset}_general.csv",
        )