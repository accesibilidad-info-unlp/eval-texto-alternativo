from pathlib import Path

IA_DIR = Path("data/ia")
HUMAN_DIR = Path("data/human")

def load_pair(file_id):

    ia_path = IA_DIR / f"original-{file-id}.md"
    human_path = HUMAN_DIR / f"corregido-{file_id}.md"

    errors = []

    if not ia_path.exists():


