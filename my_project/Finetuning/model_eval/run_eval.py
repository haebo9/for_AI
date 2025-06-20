import argparse
from model_eval.functions.main_eval import kbs_eval, type_eval, llm_eval

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--general", type=lambda x: x.lower() == "true", default=False, help="일반화 평가도 함께 실행 (True/False)")
    parser.add_argument("--kobert", type=lambda x: x.lower() == "true", default=False, help="KoBERTScore 평가 실행")
    parser.add_argument("--", type=lambda x: x.lower() == "true", default=False, help="어미 탐지 평가 실행")
    parser.add_argument("--llm", type=lambda x: x.lower() == "true", default=False, help="LLM 평가 실행")
    args = parser.parse_args()
    root_path = "/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning"
    made_filtered = ("_made" if 'made' in args.dataset else "_filtered")

    def run_all_evals(dataset_name, is_general=False):
        postfix = "_general" if is_general else ""
        input_path = f"{root_path}/dataset/_dataset/{made_filtered}/{dataset_name}{postfix}.jsonl"
        kbs_path = f"{root_path}/dataset/_dataset/_kobert/{dataset_name}{postfix}_kbs.jsonl"
        output_csv = f"{root_path}/model_eval/_csv/{dataset_name}{postfix}.csv"

        if args.kobert:
            kbs_eval(input_path, kbs_path, output_csv)
        if args.eomi:
            type_eval(input_path, output_csv)
        if args.llm:
            llm_eval(input_path, kbs_path, output_csv)

    run_all_evals(args.dataset, is_general=False)
    if args.general:
        run_all_evals(args.dataset, is_general=True)