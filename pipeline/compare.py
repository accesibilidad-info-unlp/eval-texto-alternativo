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

def compare_sections(ia:Document, human:Document):
    ia_sections = [section.heading for section in ia.sections]
    human_sections = [section.heading for section in human.sections]

    return {"section_count_delta": len(human_sections) - len(ia_sections),
            "section_coverage_ratio": len(human.sections) / max(1, len(ia.sections))}

def compare_order(ia:Document, human:Document):
    def extract_section_order(document:Document):
        return [section.heading for section in document.sections]

    ia_order = extract_section_order(ia)
    human_order = extract_section_order(human)

    return {"section_order_match": int(ia_order == human_order)}

def compare_landmarks(ia:Document, human:Document):
    def landmark_names(document:Document):
        return [landmark.name
                for section in document.sections
                for landmark in section.landmarks]

    ia_landmarks = landmark_names(ia)
    human_landmarks = landmark_names(human)

    return {"landmark_count_delta": len(human_landmarks) - len(ia_landmarks)}

def compare_documents(ia:Document, human:Document):
    return {
        **compare_structures(ia, human),
        **compare_sections(ia, human),
        **compare_order(ia, human),
        **compare_landmarks(ia, human),
    }