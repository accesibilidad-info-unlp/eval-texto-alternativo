from pathlib import Path

IA_PATTERN = "data/ia/original-{}.md"
HUMAN_PATTERN = "data/human/corregido-{}.md"

def load_pairs(start, end):
    """
    Carga los pares IA/humano del conjunto de evaluación.
    Verifica que ambos archivos existan antes de leerlos.
    """

    pairs = []

    for number in range(start, end + 1):
        document_id = f"{number:02d}"

        ia_path = Path(IA_PATTERN.format(document_id))
        human_path = Path(HUMAN_PATTERN.format(document_id))

        missing = []

        if not ia_path.exists():
            missing.append(str(ia_path))

        if not human_path.exists():
            missing.append(str(human_path))

        if missing:
            raise FileNotFoundError(
                "Missing files:\n" + "\n".join(missing)
            )

        pairs.append({
            "id": document_id,
            "ia": ia_path.read_text(encoding="utf-8"),
            "human": human_path.read_text(encoding="utf-8"),
        })

    return pairs