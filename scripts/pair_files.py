from pathlib import Path

IA_DIR = Path("data/ia")
HUMAN_DIR = Path("data/human")

IA_PREFIX = "original-"
HUMAN_PREFIX = "corregido-"

def load_pair(file_id):

    ia_path = IA_DIR / f"{IA_PREFIX}{file_id}.md"
    human_path = HUMAN_DIR / f"{HUMAN_PREFIX}{file_id}.md"

    errors = []

    if not ia_path.exists():
        errors.append(f"IA file not found: {ia_path}")

    if not human_path.exists():
        errors.append(f"Human file not found: {human_path}")

    if errors:
        raise FileNotFoundError("\n".join(errors))

    ia_text = ia_path.read_text(encoding="utf-8")
    human_text = human_path.read_text(encoding="utf-8")

    return ia_text, human_text