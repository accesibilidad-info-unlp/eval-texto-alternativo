def compare_structures(ia, human):

    return {
        "h1_added":
            int(ia["h1"] is None
            and human["h1"] is not None),
        "h2_added":
            max(0, len(human["h2"]) - len(ia["h2"])),
        "landmarks_added":
            max(0, len(human["landmarks"]) - len(ia["landmarks"])),
        "editorial_labels_added":
            max(0, len(human["editorial_labels"]) - len(ia["editorial_labels"])),
        "paragraph_added":
            human["paragraph_count"] - ia["paragraph_count"],
        "list_added":
            max(0, human["list_count"] - ia["list_count"])
    }