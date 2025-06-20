import argparse
from model_eval.functions._kobert_eval import kbs_eval
from model_eval.functions._type_eval import type_eval
from model_eval.functions._llm_eval import llm_eval
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--general", type=lambda x: x.lower() == "true", default=False)
    parser.add_argument("--kobert", type=lambda x: x.lower() == "true", default=False)
    parser.add_argument("--eomi", type=lambda x: x.lower() == "true", default=False)
    parser.add_argument("--llm", type=lambda x: x.lower() == "true", default=False)
    args = parser.parse_args()
    root_path = "/Users/jaeseoksee/Documents/project/for_AI/my_project/Finetuning"
    made_filtered = ("_made" if 'made' in args.dataset else "_filtered")

    def run_all_evals(dataset_name, is_general=False):
        postfix = "_general" if is_general else ""
        input_path = f"{root_path}/dataset/_dataset/{made_filtered}/{dataset_name}{postfix}.jsonl"
        kbs_path = f"{root_path}/dataset/_dataset/_kobert/{dataset_name}{postfix}_kbs.jsonl"
        output_csv = f"{root_path}/model_eval/_csv/{dataset_name}{postfix}_all.csv"

        all_results = []
        # 평가별로 결과 합치기
        if args.kobert:
            kbs_results = kbs_eval(input_path, kbs_path)
            all_results = kbs_results
        if args.eomi:
            eomi_results = type_eval(input_path)
            # 결과 병합 (필드가 다를 수 있으니, 필요시 merge logic 추가)
            if not all_results:
                all_results = eomi_results
            else:
                for i, r in enumerate(eomi_results):
                    all_results[i].update(r)
        if args.llm:
            llm_results = llm_eval(input_path, kbs_path)
            if not all_results:
                all_results = llm_results
            else:
                for i, r in enumerate(llm_results):
                    all_results[i].update(r)

        # CSV 저장 (최종 결과)
        if all_results:
            with open(output_csv, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
                writer.writeheader()
                writer.writerows(all_results)
            print(f"최종 결과가 {output_csv}에 저장되었습니다.")

    run_all_evals(args.dataset, is_general=False)
    if args.general:
        run_all_evals(args.dataset, is_general=True)