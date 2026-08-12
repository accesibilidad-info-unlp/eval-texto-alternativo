# structure eval

def evaluate_structure(ia, human):
    """Compara la estructura generada por IA con la corrección humana."""

    ia_structure = ia.structure
    human_structure = human.structure

    ia_counts = count_structure(ia_structure)
    human_counts = count_structure(human_structure)

    evaluation = {
        "reference": "human",
        "total_elements": {
            "ia": len(ia_structure),
            "human": len(human_structure),
        },
        "elements": {},
    }

    for element_type, label in [
        ("h1", "encabezados H1"),
        ("h2", "encabezados H2"),
        ("h3", "encabezados H3"),
        ("landmark", "landmarks"),
        ("label", "subtítulos o etiquetas"),
        ("paragraph", "párrafos"),
        ("list", "listas"),
    ]:
        ia_count = ia_counts.get(element_type, 0)
        human_count = human_counts.get(element_type, 0)

        evaluation["elements"][element_type] = {
            "ia": ia_count,
            "human": human_count,
            "difference": ia_count - human_count,
            "message": describe_difference(
                label,
                ia_count,
                human_count,
            ),
        }

    evaluation["order"] = compare_order(
        ia_structure,
        human_structure,
    )

    return evaluation


def count_structure(structure):
    """Cuenta los elementos de cada tipo dentro de una estructura."""

    counts = {}

    for element_type, _ in structure:
        counts[element_type] = counts.get(element_type, 0) + 1

    return counts


def describe_difference(label, ia_count, human_count):
    """Genera una explicación de la diferencia respecto de la referencia humana."""

    if ia_count == human_count:
        return (
            f"La IA generó {ia_count} {label}, "
            f"la misma cantidad que la corrección humana."
        )

    if ia_count < human_count:
        difference = human_count - ia_count

        return (
            f"La IA generó {ia_count} {label}, "
            f"{difference} menos que la corrección humana "
            f"({human_count})."
        )

    difference = ia_count - human_count

    return (
        f"La IA generó {ia_count} {label}, "
        f"{difference} más que la corrección humana "
        f"({human_count})."
    )


def compare_order(ia_structure, human_structure):
    """Compara los tipos de elementos según su posición en la estructura."""

    matches = 0
    comparisons = min(
        len(ia_structure),
        len(human_structure),
    )

    for position in range(comparisons):
        ia_type = ia_structure[position][0]
        human_type = human_structure[position][0]

        if ia_type == human_type:
            matches += 1

    return {
        "ia_positions": len(ia_structure),
        "human_positions": len(human_structure),
        "compared_positions": comparisons,
        "matching_positions": matches,
        "message": describe_order(
            matches,
            comparisons,
            len(ia_structure),
            len(human_structure),
        ),
    }


def describe_order(
    matches,
    comparisons,
    ia_total,
    human_total,
):
    """Genera una explicación de la comparación posicional."""

    if comparisons == 0:
        return "No hay elementos estructurales para comparar."

    if matches == comparisons and ia_total == human_total:
        return (
            "La estructura generada por la IA coincide "
            "con la corrección humana en todas las posiciones comparadas."
        )

    return (
        f"La estructura generada por la IA coincide con la "
        f"corrección humana en {matches} de {comparisons} "
        f"posiciones comparables."
    )


# content eval

def evaluate_content(ia, human):
    """Compara el contenido estructurado generado por IA con la corrección humana."""

    ia_content = ia.content
    human_content = human.content

    evaluation = {
        "reference": "human",
        "sections": {},
    }

    for heading_type, label in [
        ("h1", "encabezados H1"),
        ("h2", "encabezados H2"),
        ("h3", "encabezados H3"),
    ]:
        ia_count = len(ia_content["headings"].get(heading_type, []))
        human_count = len(human_content["headings"].get(heading_type, []))

        evaluation["sections"][heading_type] = {
            "ia": ia_count,
            "human": human_count,
            "difference": ia_count - human_count,
            "message": describe_difference(
                label,
                ia_count,
                human_count,
            ),
        }

    for section, label in [
        ("labels", "subtítulos o etiquetas"),
        ("landmarks", "landmarks"),
        ("paragraphs", "párrafos"),
        ("lists", "listas"),
    ]:
        ia_count = count_content_items(
            ia_content.get(section, {})
        )
        human_count = count_content_items(
            human_content.get(section, {})
        )

        evaluation["sections"][section] = {
            "ia": ia_count,
            "human": human_count,
            "difference": ia_count - human_count,
            "message": describe_difference(
                label,
                ia_count,
                human_count,
            ),
        }

    return evaluation


def count_content_items(content):
    """Cuenta los elementos de una colección de contenido."""

    return len(content)


# document

def evaluate_documents(ia, human):
    """Ejecuta las evaluaciones disponibles."""

    return {
        "structure": evaluate_structure(ia, human),
        "content": evaluate_content(ia, human),
    }