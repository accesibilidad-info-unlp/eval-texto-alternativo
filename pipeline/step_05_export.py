import csv
import json

def export_csv(rows, path):
    if not rows:
        return

    keys = rows[0].keys()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)

def export_json(rows, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def export_summary(summary, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

def generate_summary(rows):
    if not rows:
        return {}
    total = len(rows)

    def average(key):
        return round(sum(row[key] for row in rows) / total, 2)

    return {
        "document_count": total,
        "avg_section_heading_delta": average("section_heading_count_delta"),
        "avg_spatial_landmark_delta": average("spatial_landmark_count_delta"),
        "avg_textual_label_delta": average("textual_label_count_delta"),
        "avg_paragraph_delta": average("paragraph_count_delta"),
        "avg_list_delta": average("list_count_delta"),
    }