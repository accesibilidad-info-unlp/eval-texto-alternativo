from dataclasses import dataclass, field
import hashlib
import re
import unicodedata

@dataclass
class Document:
    structure: list[tuple[str, str]] = field(default_factory=list)
    content: dict = field(default_factory=lambda: {
        "headings": {
            "h1": [],
            "h2": []
        },
        "labels": [],
        "landmarks": [],
        "paragraphs": {},
        "lists": []
    })


def normalize_text(text):
    """Normaliza un texto para generar claves de comparación."""

    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )

    return text


def make_paragraph_key(text):
    """Genera una clave legible y compacta para un párrafo."""

    normalized = normalize_text(text)
    words = re.findall(r"\w+", normalized)

    prefix = "-".join(words[:5])
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:8]

    return f"{prefix}-{digest}"


def add_paragraph(document, text):
    key = make_paragraph_key(text)

    # Conservamos el texto original para evaluarlo posteriormente.
    document.content["paragraphs"][key] = text

    # La estructura sólo necesita una referencia breve al contenido.
    preview = " ".join(text.split()[:5])
    document.structure.append(("paragraph", preview))


def parse_document(text):
    document = Document()

    for block in text.split("\n\n"):
        block = block.strip()

        if not block:
            continue

        # Título principal.
        if block.startswith("# "):
            title = block[2:].strip()
            document.content["headings"]["h1"].append(title)
            document.structure.append(("h1", title))
            continue

        # Encabezado de sección.
        if block.startswith("## "):
            heading = block[3:].strip()
            document.content["headings"]["h2"].append(heading)
            document.structure.append(("h2", heading))
            continue

        # Landmark espacial.
        if block.startswith("[") and block.endswith("]"):
            landmark = block[1:-1].strip()
            document.content["landmarks"].append(landmark)
            document.structure.append(("landmark", landmark))
            continue

        # Etiqueta en negrita.
        if block.startswith("**") and block.endswith("**"):
            label = block[2:-2].strip()
            document.content["labels"].append(label)
            document.structure.append(("label", label))
            continue

        # Variante de etiqueta.
        if block.startswith("- ") and block.endswith(":"):
            label = block[2:-1].strip()
            document.content["labels"].append(label)
            document.structure.append(("label", label))
            continue

        # Lista.
        if block.startswith("- "):
            items = [
                line[2:].strip()
                for line in block.splitlines()
                if line.strip().startswith("- ")
            ]

            document.content["lists"].append(items)

            preview = " ".join(items[:2])
            document.structure.append(("list", preview))
            continue

        # Párrafo.
        add_paragraph(document, block)

    return document