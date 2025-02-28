from ie_datasets.datasets.tplinker.webnlg.load import load_schema, load_units


def get_summary() -> str:
    lines: list[str] = []

    lines.append("=" * 80)
    schema = load_schema()

    lines.append(f"RELATION TYPES: {schema.num_relation_types} types")
    for relation_type in schema.relation_types:
        lines.append(f"  {relation_type.id:3d}: {relation_type.name}")

    for split in ("train", "valid", "test"):
        lines.append("=" * 80)
        units = list(load_units(split=split))
        lines.append(f"{split.upper()}: {len(units)} units")
        if split != "train":
            L = max(len(unit.id) for unit in units)
            for unit in units:
                lines.append(f"  {unit.id.rjust(L)}: {unit.num_chars:3d} chars, {unit.num_entities:2d} entities, {unit.num_relations:2d} relations")

    return "\n".join(lines)


__all__ = [
    "get_summary",
]
