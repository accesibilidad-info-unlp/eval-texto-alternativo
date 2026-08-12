from step_01_pair import load_all_pairs
from step_02_preprocess import preprocess
from step_03_parse import parse_document
from step_04_eval import compare_documents
from step_05_export import (
    export_csv,
    export_json,
    export_summary,
    generate_summary
)

def main():

    ini = 1
    fin = 53

    dataset = load_all_pairs(ini, fin)
    results = []

    for pair in dataset:
        ia_raw, human_raw = pair["ia"], pair["human"]

        ia = preprocess(ia_raw)
        human = preprocess(human_raw)

        ia_document = parse_document(ia)
        human_document = parse_document(human)

        comparison = compare_documents(ia_document, human_document)
        comparison["id"] = pair["id"]

        results.append(comparison)

    export_csv(results, "outputs/comparison.csv")
    export_json(results, "outputs/comparison.json")
    export_summary(
        generate_summary(results),
        "outputs/summary.json"
    )

if __name__ == "__main__":
    main()