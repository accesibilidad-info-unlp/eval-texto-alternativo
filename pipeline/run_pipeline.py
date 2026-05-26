from pair_files import load_all_pairs
from preprocess import preprocess
from parse_md import parse_document
from compare import compare_documents
from export import (
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