from ie_datasets.datasets.hyperred.load import load_units


def get_summary() -> str:
    lines: list[str] = []

    for split in ("train", "validation", "test"):
        lines.append("=" * 80)
        units = list(load_units(split))
        lines.append(f"{split.upper()}: {len(units)} units")
        if split != "train":
            for i, unit in enumerate(units):
                lines.append(f"  {i:4d}: {unit.num_tokens:3d} tokens, {unit.num_entities:2d} entities, {unit.num_relations:2d} relations")

    return "\n".join(lines)


__all__ = [
    "get_summary",
]
