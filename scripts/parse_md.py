import re
from re import findall


def extract_h1(text):

    match = re.search(r"^# (.*)", text, flags=re.MULTILINE)

    return match.group(1) if match else None

def extract_h2(text):

    return re.findall(r"^## (.*)", text, flags=re.MULTILINE)

def extract_landmarks(text):

    return re.findall(r"^\[(.+?)\]$", text, flags=re.MULTILINE)

def count_lists(text):

    return len(findall(r"^- ", text, flags=re.MULTILINE))

def count_paragraphs(text):

    paragraphs = re.split(r"\n\s*\n", text.strip())

    return len([p for p in paragraphs if p.strip()])

def parse_document(text):

    return {
        "h1": extract_h1(text),
        "h2": extract_h2(text),
        "landmarks": extract_landmarks(text),
        "paragraph_count": count_paragraphs(text),
        "list_count": count_lists(text)
    }