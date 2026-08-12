from pathlib import Path
from types import SimpleNamespace

from pipeline.step_03_build_document import build_document
from pipeline.step_04_eval import (
    compare_order,
    count_structure,
    describe_difference,
    evaluate_content,
    evaluate_documents,
    evaluate_paragraphs,
    evaluate_structure,
)

DATA_DIR = Path("data")


# structure eval

def make_document(structure):
    """Construye un Document mínimo a partir de una estructura."""

    lines = []

    for element_type, value in structure:
        if element_type == "h1":
            lines.append(f"# {value}")
        elif element_type == "h2":
            lines.append(f"## {value}")
        elif element_type == "h3":
            lines.append(f"### {value}")
        elif element_type == "landmark":
            lines.append(f"[{value}]")
        elif element_type == "label":
            lines.append(f"**{value}**")
        elif element_type == "paragraph":
            lines.append(value)
        elif element_type == "list":
            lines.extend(f"- {item}" for item in value)

        lines.append("")

    return build_document("\n".join(lines))


def test_count_structure():
    structure = [
        ("h1", "Título"),
        ("h2", "Sección"),
        ("paragraph", "Texto"),
        ("paragraph", "Otro texto"),
        ("landmark", "Columna izquierda"),
        ("list", ["Uno", "Dos"]),
    ]

    result = count_structure(structure)

    assert result == {
        "h1": 1,
        "h2": 1,
        "paragraph": 2,
        "landmark": 1,
        "list": 1,
    }


def test_describe_difference_when_equal():
    result = describe_difference(
        "encabezados H2",
        2,
        2,
    )

    assert result == (
        "La IA generó 2 encabezados H2, "
        "la misma cantidad que la corrección humana."
    )


def test_describe_difference_when_ia_has_fewer():
    result = describe_difference(
        "landmarks",
        0,
        2,
    )

    assert result == (
        "La IA generó 0 landmarks, "
        "2 menos que la corrección humana (2)."
    )


def test_describe_difference_when_ia_has_more():
    result = describe_difference(
        "encabezados H3",
        3,
        0,
    )

    assert result == (
        "La IA generó 3 encabezados H3, "
        "3 más que la corrección humana (0)."
    )


def test_compare_order_when_structures_are_equal():
    ia = [
        ("h1", "Título"),
        ("h2", "Sección"),
        ("paragraph", "Texto"),
    ]

    human = [
        ("h1", "Título"),
        ("h2", "Sección"),
        ("paragraph", "Texto"),
    ]

    result = compare_order(ia, human)

    assert result["ia_positions"] == 3
    assert result["human_positions"] == 3
    assert result["compared_positions"] == 3
    assert result["matching_positions"] == 3


def test_compare_order_detects_different_types():
    ia = [
        ("h1", "Título"),
        ("h2", "Sección"),
        ("paragraph", "Texto"),
    ]

    human = [
        ("h1", "Título"),
        ("landmark", "Sección"),
        ("paragraph", "Texto"),
    ]

    result = compare_order(ia, human)

    assert result["matching_positions"] == 2
    assert result["compared_positions"] == 3


def test_compare_order_only_compares_existing_positions():
    ia = [
        ("h1", "Título"),
        ("h2", "Sección"),
    ]

    human = [
        ("h1", "Título"),
        ("h2", "Sección"),
        ("paragraph", "Texto"),
    ]

    result = compare_order(ia, human)

    assert result["ia_positions"] == 2
    assert result["human_positions"] == 3
    assert result["compared_positions"] == 2
    assert result["matching_positions"] == 2


def test_evaluate_structure():
    ia = make_document(
        [
            ("h1", "Título"),
            ("h2", "Sección"),
            ("paragraph", "Texto"),
        ]
    )

    human = make_document(
        [
            ("h1", "Título"),
            ("h2", "Sección"),
            ("landmark", "Columna"),
            ("paragraph", "Texto"),
        ]
    )

    result = evaluate_structure(ia, human)

    assert "reference" not in result

    assert result["total_elements"]["ia"] == 3
    assert result["total_elements"]["human"] == 4

    assert result["elements"]["h1"]["ia"] == 1
    assert result["elements"]["h1"]["human"] == 1
    assert result["elements"]["h1"]["difference"] == 0

    assert result["elements"]["landmark"]["ia"] == 0
    assert result["elements"]["landmark"]["human"] == 1
    assert result["elements"]["landmark"]["difference"] == -1

    assert result["order"]["matching_positions"] == 2


def test_evaluate_documents_contains_structure_and_content():
    ia = make_document(
        [
            ("h1", "Título"),
            ("paragraph", "Texto"),
        ]
    )

    human = make_document(
        [
            ("h1", "Título"),
            ("paragraph", "Texto"),
        ]
    )

    result = evaluate_documents(ia, human)

    assert "structure" in result
    assert "content" in result

    assert "reference" not in result["structure"]
    assert "reference" not in result["content"]


def test_real_pair_01():
    ia_path = DATA_DIR / "ia" / "original-01.md"
    human_path = DATA_DIR / "human" / "corregido-01.md"

    ia = build_document(
        ia_path.read_text(encoding="utf-8")
    )

    human = build_document(
        human_path.read_text(encoding="utf-8")
    )

    result = evaluate_structure(ia, human)

    assert "reference" not in result

    assert result["elements"]["h1"]["ia"] == 1
    assert result["elements"]["h1"]["human"] == 1

    assert result["elements"]["h3"]["ia"] == 3
    assert result["elements"]["h3"]["human"] == 0

    assert result["elements"]["landmark"]["ia"] == 0
    assert result["elements"]["landmark"]["human"] == 2


# paragraph eval

def test_evaluate_paragraphs_matches_by_key():
    """Los párrafos con la misma clave deben coincidir directamente."""

    ia = {
        "primer-parrafo-12345678": "Texto del primer párrafo.",
        "segundo-parrafo-87654321": (
            "Las universidades necesitan mejorar "
            "sus sistemas de accesibilidad."
        ),
    }

    human = {
        "primer-parrafo-12345678": "Texto del primer párrafo.",
        "tercer-parrafo-11111111": (
            "La programación funcional utiliza funciones "
            "como unidad fundamental."
        ),
    }

    result = evaluate_paragraphs(ia, human)

    assert len(result["exact_matches"]) == 1

    match = result["exact_matches"][0]

    assert match["ia_text"] == "Texto del primer párrafo."
    assert match["human_text"] == "Texto del primer párrafo."
    assert match["similarity"] == 1.0

    assert result["unmatched_ia"] == [
        "Las universidades necesitan mejorar "
        "sus sistemas de accesibilidad."
    ]

    assert result["unmatched_human"] == [
        "La programación funcional utiliza funciones "
        "como unidad fundamental."
    ]


def test_evaluate_paragraphs_uses_fuzzy_matching():
    """Los párrafos sin coincidencia por clave deben compararse por similitud."""

    ia = {
        "primer-parrafo-12345678": (
            "Las mujeres también fueron protagonistas "
            "en la historia."
        )
    }

    human = {
        "primer-parrafo-87654321": (
            "Las mujeres también fueron protagonistas "
            "de la historia."
        )
    }

    result = evaluate_paragraphs(ia, human)

    assert len(result["exact_matches"]) == 0
    assert len(result["fuzzy_matches"]) == 1

    match = result["fuzzy_matches"][0]

    assert match["ia_text"] == ia["primer-parrafo-12345678"]
    assert match["human_text"] == human["primer-parrafo-87654321"]
    assert match["similarity"] >= 0.70

    assert result["unmatched_ia"] == []
    assert result["unmatched_human"] == []


def test_evaluate_paragraphs_does_not_match_below_threshold():
    """Los párrafos con baja similitud deben quedar sin coincidencia."""

    ia = {
        "primer-parrafo-12345678": (
            "Las mujeres también fueron protagonistas."
        )
    }

    human = {
        "otro-parrafo-87654321": (
            "La computación cuántica utiliza principios "
            "de la mecánica cuántica."
        )
    }

    result = evaluate_paragraphs(ia, human)

    assert result["exact_matches"] == []
    assert result["fuzzy_matches"] == []

    assert result["unmatched_ia"] == [
        ia["primer-parrafo-12345678"]
    ]

    assert result["unmatched_human"] == [
        human["otro-parrafo-87654321"]
    ]


def test_evaluate_paragraphs_does_not_reuse_human_paragraph():
    """Un mismo párrafo humano no puede coincidir con dos párrafos de IA."""

    ia = {
        "primer-parrafo-11111111": (
            "Las mujeres fueron protagonistas "
            "de la historia."
        ),
        "segundo-parrafo-22222222": (
            "Las mujeres fueron protagonistas "
            "en la historia."
        ),
    }

    human = {
        "parrafo-humano-33333333": (
            "Las mujeres fueron protagonistas "
            "de la historia."
        ),
    }

    result = evaluate_paragraphs(ia, human)

    assert len(result["fuzzy_matches"]) == 1
    assert len(result["unmatched_ia"]) == 1
    assert len(result["unmatched_human"]) == 0


def test_evaluate_paragraphs_handles_empty_collections():
    """La comparación debe manejar colecciones vacías."""

    result = evaluate_paragraphs({}, {})

    assert result == {
        "exact_matches": [],
        "fuzzy_matches": [],
        "unmatched_ia": [],
        "unmatched_human": [],
    }


# content eval

def test_evaluate_content_compares_headings():
    """La evaluación debe comparar cada nivel de encabezado."""

    ia = SimpleNamespace(
        content={
            "headings": {
                "h1": ["Título"],
                "h2": ["Sección 1", "Sección 2"],
                "h3": ["Subsección"],
            },
            "labels": [],
            "landmarks": [],
            "paragraphs": {},
            "lists": [],
        }
    )

    human = SimpleNamespace(
        content={
            "headings": {
                "h1": ["Título"],
                "h2": ["Sección 1"],
                "h3": ["Subsección"],
            },
            "labels": [],
            "landmarks": [],
            "paragraphs": {},
            "lists": [],
        }
    )

    evaluation = evaluate_content(ia, human)

    assert "reference" not in evaluation

    assert evaluation["sections"]["h1"]["ia"] == 1
    assert evaluation["sections"]["h1"]["human"] == 1
    assert evaluation["sections"]["h1"]["difference"] == 0

    assert evaluation["sections"]["h2"]["ia"] == 2
    assert evaluation["sections"]["h2"]["human"] == 1
    assert evaluation["sections"]["h2"]["difference"] == 1

    assert evaluation["sections"]["h3"]["ia"] == 1
    assert evaluation["sections"]["h3"]["human"] == 1
    assert evaluation["sections"]["h3"]["difference"] == 0


def test_evaluate_content_compares_all_sections():
    """La evaluación debe comparar todas las colecciones de contenido."""

    ia = SimpleNamespace(
        content={
            "headings": {
                "h1": [],
                "h2": [],
                "h3": [],
            },
            "labels": ["Imagen 1"],
            "landmarks": ["main"],
            "paragraphs": {
                "primer-parrafo-12345678": "Texto"
            },
            "lists": ["lista"],
        }
    )

    human = SimpleNamespace(
        content={
            "headings": {
                "h1": [],
                "h2": [],
                "h3": [],
            },
            "labels": ["Imagen 1", "Imagen 2"],
            "landmarks": ["main", "navigation"],
            "paragraphs": {
                "primer-parrafo-12345678": "Texto",
                "segundo-parrafo-87654321": (
                    "La programación funcional utiliza funciones "
                    "como unidad fundamental."
                ),
            },
            "lists": ["lista"],
        }
    )

    evaluation = evaluate_content(ia, human)

    assert evaluation["sections"]["labels"]["ia"] == 1
    assert evaluation["sections"]["labels"]["human"] == 2
    assert evaluation["sections"]["labels"]["difference"] == -1

    assert evaluation["sections"]["landmarks"]["ia"] == 1
    assert evaluation["sections"]["landmarks"]["human"] == 2
    assert evaluation["sections"]["landmarks"]["difference"] == -1

    paragraphs = evaluation["sections"]["paragraphs"]

    assert len(paragraphs["exact_matches"]) == 1
    assert len(paragraphs["fuzzy_matches"]) == 0

    assert paragraphs["unmatched_ia"] == []
    assert paragraphs["unmatched_human"] == [
        "La programación funcional utiliza funciones "
        "como unidad fundamental."
    ]

    assert evaluation["sections"]["lists"]["ia"] == 1
    assert evaluation["sections"]["lists"]["human"] == 1
    assert evaluation["sections"]["lists"]["difference"] == 0


def test_evaluate_content_handles_empty_content():
    """La evaluación debe manejar colecciones de contenido vacías."""

    empty_content = {
        "headings": {},
        "labels": [],
        "landmarks": [],
        "paragraphs": {},
        "lists": [],
    }

    ia = SimpleNamespace(content=empty_content)
    human = SimpleNamespace(content=empty_content)

    evaluation = evaluate_content(ia, human)

    for section in (
        "h1",
        "h2",
        "h3",
        "labels",
        "landmarks",
        "lists",
    ):
        assert evaluation["sections"][section]["ia"] == 0
        assert evaluation["sections"][section]["human"] == 0
        assert evaluation["sections"][section]["difference"] == 0

    assert evaluation["sections"]["paragraphs"] == {
        "exact_matches": [],
        "fuzzy_matches": [],
        "unmatched_ia": [],
        "unmatched_human": [],
    }