def compare_structures(ia, human):

    return {
        "document_title_introduced":
            int(ia["document_title"] is None
            and human["document_title"] is not None),
        "section_heading_count_delta":
            max(0, len(human["section_headings"]) - len(ia["section_headings"])),
        "spatial_landmark_count_delta":
            max(0, len(human["spatial_landmarks"]) - len(ia["spatial_landmarks"])),
        "textual_label_count_delta":
            max(0, len(human["textual_labels"]) - len(ia["textual_labels"])),
        "paragraph_count_delta":
            human["paragraph_count"] - ia["paragraph_count"],
        "list_count_delta":
            max(0, human["list_count"] - ia["list_count"])
    }