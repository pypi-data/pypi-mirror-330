from ie_datasets.datasets.re_docred.load import load_schema, load_units


def get_summary() -> str:
    lines: list[str] = []

    schema = load_schema()
    lines.append("=" * 80)
    lines.append("RELATION TYPES")
    L = max(len(relation_type.id) for relation_type in schema.relation_types)
    for relation_type in schema.relation_types:
        lines.append(f"  {relation_type.id.rjust(L)}: {relation_type.description}")

    for split in ("train", "dev", "test"):
        units = list(load_units(split=split))

        lines.append("=" * 80)
        lines.append(f"{split.upper()}: {len(units)} units")

        L = max(len(str(unit.title)) for unit in units)
        for unit in units:
            lines.append(f"  {str(unit.title).rjust(L)}: {unit.num_tokens:3d} tokens, {unit.num_sentences:2d} sentences, {unit.num_entities:2d} entities, {unit.num_relations:2d} relations")

    return "\n".join(lines)


__all__ = [
    "get_summary"
]
