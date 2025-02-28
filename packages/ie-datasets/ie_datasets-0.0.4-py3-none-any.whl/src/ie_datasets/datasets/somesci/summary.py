from typing import Optional

from ie_datasets.datasets.somesci.load import (
    load_schema,
    load_units,
    SoMeSciVersion,
)


def get_summary(
        version: Optional[SoMeSciVersion] = None,
) -> str:
    lines: list[str] = []

    schema = load_schema(version=version)
    lines.append("=" * 80)
    lines.append("SCHEMA")
    lines.append("-" * 80)
    lines.append(f"ENTITY TYPES: {len(schema.entity_types)} types")
    for t in schema.entity_types:
        lines.append(f"  {t.name}")
    lines.append("-" * 80)
    lines.append(f"RELATION TYPES: {len(schema.relation_types)} types")
    for t in schema.relation_types:
        lines.append(f"  {t.name}(")
        lines.append(f"    {'|'.join(t.argument_1_types)},")
        lines.append(f"    {'|'.join(t.argument_2_types)}")
        lines.append(f"  )")

    for group in ("Creation_sentences", "PLoS_methods", "PLoS_sentences", "Pubmed_fulltext"):
        for split in ("train", "devel", "test"):
            units = list(load_units(version=version, group=group, split=split))
            lines.append("=" * 80)
            lines.append(f"{group}/{split.upper()}: {len(units)} units")
            L = max(0 if unit.id is None else len(unit.id) for unit in units)
            for unit in units:
                id = "" if unit.id is None else unit.id
                lines.append(f"  {id.rjust(L)}: {unit.num_chars:6d} chars, {unit.num_entities:2d} entities, {unit.num_relations:2d} relations")

    return "\n".join(lines)


__all__ = [
    "get_summary",
]
