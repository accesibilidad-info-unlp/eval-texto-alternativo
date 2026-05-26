from parse_md import Document


def compare_structures(ia:Document, human:Document):

    return {
        "document_title_introduced":
            int(ia.title is None and
                human.title is not None),
        "section_heading_count_delta":
            human.metrics.section_heading_count - ia.metrics.section_heading_count,
        "spatial_landmark_count_delta":
            human.metrics.spatial_landmark_count - ia.metrics.spatial_landmark_count,
        "textual_label_count_delta":
            human.metrics.textual_label_count - ia.metrics.textual_label_count,
        "paragraph_count_delta":
            human.metrics.paragraph_count - ia.metrics.paragraph_count,
        "list_count_delta":
            human.metrics.list_count - ia.metrics.list_count,
    }