from pathlib import Path

from pipeline.step_03_parse import (
    make_paragraph_key,
    normalize_text,
    parse_document,
)
from pipeline.step_02_preprocess import preprocess


REAL_FILES = [
    Path("data/ia/original-01.md"),
    Path("data/human/corregido-01.md"),
    Path("data/ia/original-53.md"),
    Path("data/human/corregido-53.md"),
]


def parse_real_file(path):
    text = path.read_text(encoding="utf-8")
    return parse_document(preprocess(text))


def test_real_files_produce_documents():
    """Los documentos reales deben poder ser parseados."""
    for path in REAL_FILES:
        document = parse_real_file(path)

        assert document is not None
        assert isinstance(document.structure, list)
        assert isinstance(document.content, dict)


def test_real_documents_have_expected_content_sections():
    """El modelo debe exponer las colecciones utilizadas por los evaluadores."""
    for path in REAL_FILES:
        document = parse_real_file(path)

        assert set(document.content) == {
            "headings",
            "labels",
            "landmarks",
            "paragraphs",
            "lists",
        }

        assert set(document.content["headings"]) == {"h1", "h2"}


def test_real_documents_have_structural_elements():
    """Los documentos reales deben generar elementos en su secuencia estructural."""
    for path in REAL_FILES:
        document = parse_real_file(path)

        assert document.structure

        for element_type, value in document.structure:
            assert element_type in {
                "h1",
                "h2",
                "landmark",
                "label",
                "list",
                "paragraph",
            }
            assert isinstance(value, str)


def test_real_paragraph_keys_are_compact():
    """Las claves reales deben conservar un prefijo legible y un hash corto."""
    for path in REAL_FILES:
        document = parse_real_file(path)

        for key in document.content["paragraphs"]:
            parts = key.rsplit("-", 1)

            assert len(parts) == 2
            prefix, digest = parts

            assert prefix
            assert len(digest) == 8
            assert all(char in "0123456789abcdef" for char in digest)


def test_normalize_text_ignores_case_and_accents():
    first = "LAS MUJERES TAMBIÉN FUERON PROTAGONISTAS"
    second = "Las mujeres también fueron protagonistas"

    assert normalize_text(first) == normalize_text(second)


def test_paragraph_key_uses_first_five_words_and_hash():
    text = "Las mujeres también fueron protagonistas en la historia."

    key = make_paragraph_key(text)

    assert key.startswith(
        "las-mujeres-tambien-fueron-protagonistas-"
    )

    digest = key.rsplit("-", 1)[1]
    assert len(digest) == 8


def test_same_normalized_text_produces_same_key():
    first = "LAS MUJERES TAMBIÉN FUERON PROTAGONISTAS."
    second = "Las mujeres también fueron protagonistas."

    assert make_paragraph_key(first) == make_paragraph_key(second)


def test_different_full_text_can_have_same_prefix_but_different_key():
    first = (
        "Las mujeres también fueron protagonistas "
        "en la historia de la tecnología."
    )
    second = (
        "Las mujeres también fueron protagonistas "
        "durante el desarrollo de la informática."
    )

    assert first != second
    assert make_paragraph_key(first) != make_paragraph_key(second)