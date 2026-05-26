from pair_files import load_pair
from preprocess import preprocess
from parse_md import parse_document

PAIR_ID = "08"

def main():
    ia_raw, human_raw = load_pair(PAIR_ID)

    ia = preprocess(ia_raw)
    human = preprocess(human_raw)

    ia_data = parse_document(ia)
    human_data = parse_document(human)

    print("\n=== IA structure ===\n")
    print(ia_data)

    print("\n=== Human clean ===\n")
    print(human_data)

if __name__ == "__main__":
    main()