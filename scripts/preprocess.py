import re

def remove_front_matter(text):

    if not text.startswith("---"):
        return text

    pattern =  r"^---\s*\n.*?\n---\s*\n?"

    return re.sub(pattern, "", text, flags=re.DOTALL)

def normalize_whitespace(text):

    lines = [line.strip() for line in text.splitlines()]

    return "\n".join(lines).strip()

def remove_html_tags(text):
    return re.sub(r"<[^>]+>", "", text)

def preprocess(text):

    text = remove_front_matter(text)
    text = remove_html_tags(text)
    text = normalize_whitespace(text)

    return text