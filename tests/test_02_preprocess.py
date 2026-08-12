from pathlib import Path

from pipeline.step_02_preprocess import (
    normalize_whitespace,
    preprocess,
    remove_front_matter,
    remove_backticks,
    remove_html_tags,
)


REAL_FILES = [
    Path("data/ia/original-01.md"),
    Path("data/human/corregido-01.md"),
    Path("data/ia/original-53.md"),
    Path("data/human/corregido-53.md"),
]


def test_real_files_can_be_preprocessed():
    """Los archivos reales deben poder atravesar el preprocesamiento."""
    for path in REAL_FILES:
        text = path.read_text(encoding="utf-8")
        result = preprocess(text)

        assert isinstance(result, str)
        assert result.strip()


def test_front_matter_is_removed_from_real_files():
    """El front matter de los documentos reales no debe llegar al parser."""
    for path in REAL_FILES:
        text = path.read_text(encoding="utf-8")
        result = remove_front_matter(text)

        assert not result.lstrip().startswith("---")


def test_remove_backticks():
    text = "`Cecilia Berdichevsky` y `Ada Lovelace`"

    result = remove_backticks(text)

    assert result == "Cecilia Berdichevsky y Ada Lovelace"


def test_preprocess_removes_front_matter():
    text = """---
layout: layouts/post.njk
title: Ejemplo
---

# Título
Texto
"""

    result = remove_front_matter(text)

    assert "layout: layouts/post.njk" not in result
    assert "title: Ejemplo" not in result
    assert "# Título" in result
    assert "Texto" in result


def test_preprocess_removes_html_tags():
    text = "Texto <strong>importante</strong> y <br> continuación."

    result = remove_html_tags(text)

    assert result == "Texto importante y  continuación."


def test_preprocess_normalizes_whitespace():
    text = "  Primera línea  \n\n  Segunda línea  "

    result = normalize_whitespace(text)

    assert result == "Primera línea\n\nSegunda línea"


def test_preprocess_applies_all_transformations():
    text = """---
title: Ejemplo
---

# Título

Texto <strong>importante</strong>
"""

    result = preprocess(text)

    assert "---" not in result
    assert "<strong>" not in result
    assert "</strong>" not in result
    assert result == "# Título\n\nTexto importante"