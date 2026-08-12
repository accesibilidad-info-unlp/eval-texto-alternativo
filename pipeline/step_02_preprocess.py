import re

def remove_front_matter(text):
    """Elimina el front matter utilizado por la plataforma de publicación."""

    if not text.startswith("---"):
        return text

    pattern =  r"^---\s*\n.*?\n---\s*\n?"

    return re.sub(pattern, "", text, flags=re.DOTALL)

def remove_backticks(text):
    """Elimina backticks generados por la IA.."""
    return text.replace("`", "")

def remove_html_tags(text):
    return re.sub(r"<[^>]+>", "", text)

def normalize_whitespace(text):
    lines = [line.strip() for line in text.splitlines()]

    return "\n".join(lines).strip()

def preprocess(text):
    """Prepara el texto para su posterior análisis estructural y de contenido."""

    text = remove_front_matter(text)
    text = remove_backticks(text)
    text = remove_html_tags(text)
    text = normalize_whitespace(text)

    return text