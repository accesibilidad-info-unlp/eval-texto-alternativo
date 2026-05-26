from pprint import pprint

from pair_files import load_pair
from preprocess import preprocess
from parse_md import parse_document
from compare import compare_structures

PAIR_ID = "08"

def main():
    ia_raw, human_raw = load_pair(PAIR_ID)

    ia = preprocess(ia_raw)
    human = preprocess(human_raw)

    ia_data = parse_document(ia)
    human_data = parse_document(human)

    comparison = compare_structures(ia_data, human_data)

    # print("\n=== Comparison ===\n")
    #
    # for key, value in comparison.items():
    #     print(f"{key}: {value}")

    print("\n=== Human sections ===\n")
    pprint(
        human_data["sections"],
        width=100
    )

if __name__ == "__main__":
    main()