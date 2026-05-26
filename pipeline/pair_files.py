from pathlib import Path

IA_DIR = Path("data/ia")
HUMAN_DIR = Path("data/human")

IA_PREFIX = "original-"
HUMAN_PREFIX = "corregido-"

def make_path(path, prefix, id):
    return path / f"{prefix}{id}.md"

def load_pair(file_id):

    ia_path = make_path(IA_DIR, IA_PREFIX, file_id)
    human_path = make_path(HUMAN_DIR, HUMAN_PREFIX, file_id)

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

def load_all_pairs(ini, fin):
    pairs = []
    for file in range(ini, fin+1):
        id_str = str(file).zfill(2)
        ia_path = make_path(IA_DIR, IA_PREFIX, id_str)
        human_path = make_path(HUMAN_DIR, HUMAN_PREFIX, id_str)
        pairs.append({
            "id": id_str,
            "ia": open(ia_path, encoding="utf-8").read(),
            "human": open(human_path, encoding="utf-8").read()
        })
    return pairs