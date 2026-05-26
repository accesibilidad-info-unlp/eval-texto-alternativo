import re
from re import findall


def extract_document_title(text):
    match = re.search(r"^# (.*)", text, flags=re.MULTILINE)
    return match.group(1) if match else None

def extract_section_headings(text):
    return re.findall(r"^## (.*)", text, flags=re.MULTILINE)

def extract_spatial_landmarks(text):
    return re.findall(r"^\[(.+?)\]$", text, flags=re.MULTILINE)

def count_lists(text):
    return len(findall(r"^- ", text, flags=re.MULTILINE))

def count_paragraphs(text):
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return len([p for p in paragraphs if p.strip()])

def extract_textual_labels(text):
    labels = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        # **label**
        bold_match = re.match(r"^\*\*(.+?)\*\*$", line)
        if bold_match:
            labels.append(bold_match.group(1))
            continue

        # - label:
        dash_match = re.match(r"^- (.+):$", line)
        if dash_match:
            labels.append(dash_match.group(1))

    return labels

def extract_sections(text):
    sections = []

    current_section = None
    current_landmark = None

    paragraphs = text.split("\n\n")

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        # section heading
        h2_match = re.match(r"^## (.+)$", paragraph)
        if h2_match:
            current_section = {
                "heading": h2_match.group(1),
                "landmarks": []
            }
            sections.append(current_section)
            current_landmark = None
            continue

        # landmark
        landmark_match = re.match(r"^\[(.+)\]$", paragraph)
        if landmark_match and current_section:
            current_landmark = {
                "name": landmark_match.group(1),
                "paragraph_count": 0,
                "paragraphs": []
            }
            current_section["landmarks"].append(current_landmark)
            continue

        # current paragraph
        if current_landmark:
            current_landmark["paragraph_count"] += 1
            current_landmark["paragraphs"].append(paragraph)

    return sections


def parse_document(text):

    return {
        "document_title": extract_document_title(text),
        "section_headings": extract_section_headings(text),
        "spatial_landmarks": extract_spatial_landmarks(text),
        "textual_labels": extract_textual_labels(text),
        "sections": extract_sections(text),
        "paragraph_count": count_paragraphs(text),
        "list_count": count_lists(text)
    }