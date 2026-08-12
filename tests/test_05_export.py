import json

from pipeline.step_05_export import (
    export_csv,
    export_json,
    export_summary,
    flatten_results,
    generate_summary,
)


def sample_results():
    return [
        {
            "id": 1,
            "structure": {
                "elements": {
                    "h1": {
                        "ia": 1,
                        "human": 1,
                        "difference": 0,
                    },
                    "h2": {
                        "ia": 2,
                        "human": 1,
                        "difference": 1,
                    },
                    "h3": {
                        "ia": 1,
                        "human": 2,
                        "difference": -1,
                    },
                    "landmark": {
                        "ia": 1,
                        "human": 1,
                        "difference": 0,
                    },
                    "label": {
                        "ia": 2,
                        "human": 1,
                        "difference": 1,
                    },
                    "paragraph": {
                        "ia": 10,
                        "human": 12,
                        "difference": -2,
                    },
                    "list": {
                        "ia": 1,
                        "human": 1,
                        "difference": 0,
                    },
                }
            },
            "content": {
                "sections": {},
            },
        }
    ]


def test_flatten_results():
    """Los resultados deben convertirse en filas aptas para CSV."""

    rows = flatten_results(sample_results())

    assert len(rows) == 1

    row = rows[0]

    assert row["id"] == 1

    assert row["encabezados_h1_ia"] == 1
    assert row["encabezados_h1_humano"] == 1
    assert row["diferencia_encabezados_h1"] == 0

    assert row["encabezados_h2_ia"] == 2
    assert row["encabezados_h2_humano"] == 1
    assert row["diferencia_encabezados_h2"] == 1

    assert row["encabezados_h3_ia"] == 1
    assert row["encabezados_h3_humano"] == 2
    assert row["diferencia_encabezados_h3"] == -1

    assert row["landmarks_ia"] == 1
    assert row["landmarks_humano"] == 1
    assert row["diferencia_landmarks"] == 0

    assert row["etiquetas_ia"] == 2
    assert row["etiquetas_humano"] == 1
    assert row["diferencia_etiquetas"] == 1

    assert row["parrafos_ia"] == 10
    assert row["parrafos_humano"] == 12
    assert row["diferencia_parrafos"] == -2

    assert row["listas_ia"] == 1
    assert row["listas_humano"] == 1
    assert row["diferencia_listas"] == 0


def test_generate_summary():
    """El resumen debe calcular los promedios de las diferencias."""

    summary = generate_summary(sample_results())

    assert summary == {
        "cantidad_documentos": 1,
        "promedio_diferencia_encabezados_h1": 0,
        "promedio_diferencia_encabezados_h2": 1,
        "promedio_diferencia_encabezados_h3": -1,
        "promedio_diferencia_landmarks": 0,
        "promedio_diferencia_etiquetas": 1,
        "promedio_diferencia_parrafos": -2,
        "promedio_diferencia_listas": 0,
    }


def test_generate_summary_empty():
    """Un conjunto vacío debe producir un resumen vacío."""

    assert generate_summary([]) == {}


def test_export_csv(tmp_path):
    """Los resultados deben poder exportarse a CSV."""

    path = tmp_path / "comparison.csv"

    rows = flatten_results(sample_results())

    export_csv(rows, path)

    assert path.exists()

    content = path.read_text(encoding="utf-8")

    assert "id" in content
    assert "encabezados_h3_ia" in content
    assert "diferencia_encabezados_h3" in content
    assert "parrafos_ia" in content


def test_export_csv_empty(tmp_path):
    """Una colección vacía no debe generar un archivo CSV."""

    path = tmp_path / "comparison.csv"

    export_csv([], path)

    assert not path.exists()


def test_export_json(tmp_path):
    """Los resultados completos deben conservarse en JSON."""

    path = tmp_path / "comparison.json"

    results = sample_results()

    export_json(results, path)

    assert path.exists()

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert data == results


def test_export_summary(tmp_path):
    """El resumen debe poder exportarse como JSON."""

    path = tmp_path / "summary.json"

    summary = generate_summary(sample_results())

    export_summary(summary, path)

    assert path.exists()

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    assert data == summary