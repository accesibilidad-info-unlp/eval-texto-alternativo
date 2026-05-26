from dataclasses import dataclass, field

@dataclass
class Metrics:
    section_heading_count: int = 0
    spatial_landmark_count: int = 0
    textual_label_count: int = 0
    paragraph_count: int = 0
    list_count: int = 0

@dataclass
class Landmark:
    name: str
    paragraphs: list[str] = field(default_factory=list)
    text_labels: list[str] = field(default_factory=list)
    lists: list[str] = field(default_factory=list)

@dataclass
class Section:
    heading: str
    landmarks: list[Landmark] = field(default_factory=list)
    text_labels: list[str] = field(default_factory=list)
    paragraphs: list[str] = field(default_factory=list)
    lists: list[str] = field(default_factory=list)

@dataclass
class Document:
    title: str | None = None
    sections: list[Section] = field(default_factory=list)
    metrics: Metrics = field(default_factory=Metrics)

def parse_document(text):
    document = Document()

    blocks = text.split("\n\n")

    current_section = None
    current_landmark = None

    def get_target():
        return current_landmark if current_landmark else current_section

    def compute_metrics(sections: list[Section]) -> Metrics:
        metrics = Metrics()
        metrics.section_heading_count = len(sections)

        for section in sections:
            metrics.spatial_landmark_count += len(section.landmarks)
            metrics.textual_label_count += len(section.text_labels)
            metrics.paragraph_count += len(section.paragraphs)
            metrics.list_count += len(section.lists)

            for landmark in section.landmarks:
                metrics.textual_label_count += len(landmark.text_labels)
                metrics.paragraph_count += len(landmark.paragraphs)
                metrics.list_count += len(landmark.lists)

        return metrics

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        # Extract document title
        if block.startswith("# "):
            document.title = block[2:].strip()
            continue

        # Extract section
        if block.startswith("## "):
            current_section = Section(heading = block[3:].strip())
            document.sections.append(current_section)
            current_landmark = None
        # Extract landmark
        elif block.startswith("[") and block.endswith("]"):
            if current_section is None:
                continue
            current_landmark = Landmark(name = block[1:-1].strip())
            current_section.landmarks.append(current_landmark)
        # Extract text labels
        elif block.startswith("**") and block.endswith("**"):
            label = block[2:-2].strip()
            target = get_target()
            if target:
                target.text_labels.append(label)
        # Extract label variant
        elif block.startswith("- ") and block.endswith(":"):
            label = block[2:-1].strip()
            target = get_target()
            if target:
                target.text_labels.append(label)
        # Extract list item
        elif block.startswith("- "):
            target = get_target()
            if target:
                for line in block.splitlines():
                    line = line.strip()
                    if line.startswith("- "):
                        target.lists.append(line[2:].strip())
        # Extract paragraphs
        else:
            target = get_target()
            if target:
                target.paragraphs.append(block)

    document.metrics = compute_metrics(document.sections)

    return document