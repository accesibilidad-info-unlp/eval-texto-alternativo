import csv
import json


def export_csv(rows, path):
    """Exporta filas planas a un archivo CSV."""

    if not rows:
        return

    keys = rows[0].keys()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def export_json(rows, path):
    """Exporta los resultados completos a JSON."""

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            rows,
            f,
            ensure_ascii=False,
            indent=2,
        )


def export_summary(summary, path):
    """Exporta el resumen estadístico a JSON."""

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            summary,
            f,
            ensure_ascii=False,
            indent=2,
        )


def flatten_results(results):
    """Convierte las evaluaciones en filas planas para el CSV."""

    rows = []

    for result in results:
        elements = result["structure"]["elements"]

        rows.append({
            "id": result["id"],

            "encabezados_h1_ia": elements["h1"]["ia"],
            "encabezados_h1_humano": elements["h1"]["human"],
            "diferencia_encabezados_h1": elements["h1"]["difference"],

            "encabezados_h2_ia": elements["h2"]["ia"],
            "encabezados_h2_humano": elements["h2"]["human"],
            "diferencia_encabezados_h2": elements["h2"]["difference"],

            "encabezados_h3_ia": elements["h3"]["ia"],
            "encabezados_h3_humano": elements["h3"]["human"],
            "diferencia_encabezados_h3": elements["h3"]["difference"],

            "landmarks_ia": elements["landmark"]["ia"],
            "landmarks_humano": elements["landmark"]["human"],
            "diferencia_landmarks": elements["landmark"]["difference"],

            "etiquetas_ia": elements["label"]["ia"],
            "etiquetas_humano": elements["label"]["human"],
            "diferencia_etiquetas": elements["label"]["difference"],

            "parrafos_ia": elements["paragraph"]["ia"],
            "parrafos_humano": elements["paragraph"]["human"],
            "diferencia_parrafos": elements["paragraph"]["difference"],

            "listas_ia": elements["list"]["ia"],
            "listas_humano": elements["list"]["human"],
            "diferencia_listas": elements["list"]["difference"],
        })

    return rows


def generate_summary(results):
    """Genera estadísticas agregadas de las evaluaciones."""

    if not results:
        return {}

    total = len(results)

    def average(element_type):
        return round(
            sum(
                result["structure"]["elements"][element_type]["difference"]
                for result in results
            ) / total,
            2,
        )

    return {
        "cantidad_documentos": total,
        "promedio_diferencia_encabezados_h1": average("h1"),
        "promedio_diferencia_encabezados_h2": average("h2"),
        "promedio_diferencia_encabezados_h3": average("h3"),
        "promedio_diferencia_landmarks": average("landmark"),
        "promedio_diferencia_etiquetas": average("label"),
        "promedio_diferencia_parrafos": average("paragraph"),
        "promedio_diferencia_listas": average("list"),
    }