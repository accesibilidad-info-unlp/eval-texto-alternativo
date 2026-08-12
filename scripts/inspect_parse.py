from pathlib import Path
import sys

from pipeline.step_02_preprocess import preprocess
from pipeline.step_03_parse import parse_document


DATA_DIR = Path("data")


def load_document(path):
    text = path.read_text(encoding="utf-8")
    return parse_document(preprocess(text))


def print_separator(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_structure(document):
    print("STRUCTURE")
    print("-" * 70)

    for position, (element_type, value) in enumerate(
        document.structure,
        start=1,
    ):
        print(f"{position:02d}  {element_type:<10} {value}")


def print_content(document):
    content = document.content

    print("CONTENT")
    print("-" * 70)

    print("HEADINGS")
    print(f"  H1: {content['headings']['h1']}")
    print(f"  H2: {content['headings']['h2']}")

    print("\nLABELS")
    for label in content["labels"]:
        print(f"  - {label}")

    print("\nLANDMARKS")
    for landmark in content["landmarks"]:
        print(f"  - {landmark}")

    print("\nPARAGRAPHS")
    for key, text in content["paragraphs"].items():
        print(f"  {key}")
        print(f"    {text}")

    print("\nLISTS")
    for number, items in enumerate(content["lists"], start=1):
        print(f"  List {number}:")
        for item in items:
            print(f"    - {item}")


def print_document(name, path, document):
    print_separator(name)

    print(f"FILE: {path}")

    print()
    print_structure(document)

    print()
    print("-" * 70)
    print_content(document)


def main():
    number = sys.argv[1] if len(sys.argv) > 1 else "01"

    ia_path = DATA_DIR / "ia" / f"original-{number}.md"
    human_path = DATA_DIR / "human" / f"corregido-{number}.md"

    ia_document = load_document(ia_path)
    human_document = load_document(human_path)

    print_separator(f"PARSE INSPECTION — PAIR {number}")

    print_document(
        "DOCUMENT — IA",
        ia_path,
        ia_document,
    )

    print_document(
        "DOCUMENT — HUMAN",
        human_path,
        human_document,
    )


if __name__ == "__main__":
    main()