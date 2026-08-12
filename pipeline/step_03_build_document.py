from dataclasses import dataclass, field
import hashlib
import re
import unicodedata

@dataclass
class Document:
    structure: list[tuple[str, str | list[str]]] = field(default_factory=list)
    content: dict = field(
        default_factory=lambda: {
            "headings": {
                "h1": [],
                "h2": [],
                "h3": [],
            },
            "labels": [],
            "landmarks": [],
            "paragraphs": {},
            "lists": [],
        }
    )


def normalize_text(text):
    """Normaliza el texto para generar identificadores comparables."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(
        char
        for char in text
        if unicodedata.category(char) != "Mn"
    )
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def make_paragraph_key(text):
    """Genera una clave legible y compacta para un párrafo."""
    normalized = normalize_text(text)

    words = normalized.split()
    prefix = "-".join(words[:5])

    digest = hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()[:8]

    return f"{prefix}-{digest}"


def add_paragraph(document, text):
    """Agrega un párrafo a la estructura y al contenido."""
    text = text.strip()

    if not text:
        return

    key = make_paragraph_key(text)

    document.structure.append(("paragraph", text))
    document.content["paragraphs"][key] = text


def add_list(document, items):
    """Agrega una lista como una unidad estructural."""
    if not items:
        return

    document.structure.append(("list", items))
    document.content["lists"].append(items)


def build_document(text):
    document = Document()

    lines = text.splitlines()

    paragraph_lines = []
    list_items = []

    def flush_paragraph():
        nonlocal paragraph_lines

        if paragraph_lines:
            add_paragraph(
                document,
                " ".join(paragraph_lines),
            )
            paragraph_lines = []

    def flush_list():
        nonlocal list_items

        if list_items:
            add_list(document, list_items)
            list_items = []

    for line in lines:
        line = line.strip()

        # Una línea vacía finaliza el elemento actual.
        if not line:
            flush_paragraph()
            flush_list()
            continue

        # Encabezados H1, H2 y H3.
        heading_match = re.match(
            r"^(#{1,3})\s+(.+)$",
            line,
        )

        if heading_match:
            flush_paragraph()
            flush_list()

            level = len(heading_match.group(1))
            value = heading_match.group(2).strip()
            heading = f"h{level}"

            document.structure.append(
                (heading, value)
            )
            document.content["headings"][heading].append(value)

            continue

        # Landmarks.
        if line.startswith("[") and line.endswith("]"):
            flush_paragraph()
            flush_list()

            value = line[1:-1].strip()

            document.structure.append(
                ("landmark", value)
            )
            document.content["landmarks"].append(value)

            continue

        # Subtítulos en negrita.
        if line.startswith("**") and line.endswith("**"):
            flush_paragraph()
            flush_list()

            value = line[2:-2].strip()

            document.structure.append(
                ("label", value)
            )
            document.content["labels"].append(value)

            continue

        # Inicio de un elemento de lista.
        if line.startswith("- "):
            flush_paragraph()

            list_items.append(line[2:].strip())
            continue

        # Continuación de una lista.
        if list_items:
            list_items[-1] += " " + line
            continue

        # Texto normal.
        paragraph_lines.append(line)

    flush_paragraph()
    flush_list()

    return document