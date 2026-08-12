from step_01_pair import load_pairs
from step_02_preprocess import preprocess
from step_03_build_document import build_document
from step_04_eval import evaluate_documents
from step_05_export import (
    export_csv,
    export_json,
    export_summary,
    flatten_results,
    generate_summary,
)


def main():
    start = 1
    end = 53

    dataset = load_pairs(start, end)
    results = []

    for pair in dataset:
        ia_raw = pair["ia"]
        human_raw = pair["human"]

        ia = preprocess(ia_raw)
        human = preprocess(human_raw)

        ia_document = build_document(ia)
        human_document = build_document(human)

        comparison = evaluate_documents(
            ia_document,
            human_document,
        )

        comparison["id"] = pair["id"]

        results.append(comparison)

    export_csv(
        flatten_results(results),
        "outputs/comparison.csv",
    )
    export_json(
        results,
        "outputs/comparison.json",
    )
    export_summary(
        generate_summary(results),
        "outputs/summary.json",
    )


if __name__ == "__main__":
    main()