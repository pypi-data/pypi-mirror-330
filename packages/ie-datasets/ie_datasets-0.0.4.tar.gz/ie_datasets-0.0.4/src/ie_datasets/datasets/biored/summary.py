from ie_datasets.datasets.biored.load import load_units


def get_summary() -> str:
    lines: list[str] = []

    for split in ("Train", "Dev", "Test"):
        lines.append("=" * 80)
        units = list(load_units(split))

        lines.append(f"{split.upper()}: {len(units)} units")
        L = max(len(unit.id) for unit in units)
        for unit in units:
            lines.append(f"  {unit.id.rjust(L)}: {unit.num_chars:4d} chars, {unit.num_entity_mentions:2d} entity mentions, {unit.num_entities:2d} entities, {unit.num_relations:3d} relations")

    return "\n".join(lines)
