import re

def remove_front_matter(text):
    """Elimina el front matter utilizado por la plataforma de publicación."""

    if not text.startswith("---"):
        return text

    pattern =  r"^---\s*\n.*?\n---\s*\n?"

    return re.sub(pattern, "", text, flags=re.DOTALL)

def normalize_whitespace(text):
    """Normaliza espacios y saltos de línea sin alterar el contenido textual."""

    lines = [line.strip() for line in text.splitlines()]

    return "\n".join(lines).strip()

def remove_html_tags(text):
    """Elimina etiquetas HTML que no forman parte del contenido evaluado."""
    return re.sub(r"<[^>]+>", "", text)

def preprocess(text):
    """Prepara el texto para su posterior análisis estructural y de contenido."""

    text = remove_front_matter(text)
    text = remove_html_tags(text)
    text = normalize_whitespace(text)

    return text