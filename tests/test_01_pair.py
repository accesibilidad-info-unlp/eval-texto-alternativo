from pathlib import Path

import pytest

from pipeline import step_01_pair


DATASET_SIZE = 53


def test_load_all_real_pairs():
    """Todos los pares reales del dataset deben estar completos y ser legibles."""
    pairs = step_01_pair.load_pairs(1, DATASET_SIZE)

    assert len(pairs) == DATASET_SIZE

    for number, pair in enumerate(pairs, start=1):
        document_id = f"{number:02d}"

        assert pair["id"] == document_id
        assert pair["ia"]
        assert pair["human"]
        assert pair["ia"] == Path(
            f"data/ia/original-{document_id}.md"
        ).read_text(encoding="utf-8")
        assert pair["human"] == Path(
            f"data/human/corregido-{document_id}.md"
        ).read_text(encoding="utf-8")


def test_real_dataset_has_matching_ids():
    """Los archivos IA y humano deben estar emparejados por el mismo identificador."""
    pairs = step_01_pair.load_pairs(1, DATASET_SIZE)

    assert [pair["id"] for pair in pairs] == [
        f"{number:02d}" for number in range(1, DATASET_SIZE + 1)
    ]


def test_missing_file_stops_loading(tmp_path, monkeypatch):
    """Un par incompleto debe producir un error explícito."""
    ia_pattern = str(tmp_path / "ia-original-{}.md")
    human_pattern = str(tmp_path / "human-corregido-{}.md")

    Path(ia_pattern.format("01")).write_text("IA", encoding="utf-8")

    monkeypatch.setattr(step_01_pair, "IA_PATTERN", ia_pattern)
    monkeypatch.setattr(step_01_pair, "HUMAN_PATTERN", human_pattern)

    with pytest.raises(FileNotFoundError, match="human-corregido-01.md"):
        step_01_pair.load_pairs(1, 1)