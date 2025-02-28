from ie_datasets.datasets.cuad.load import load_units


def get_summary() -> str:
    lines: list[str] = []

    units = list(load_units())

    lines.append("=" * 80)
    lines.append(f"{len(units)} units")
    L = max(len(str(unit.title)) for unit in units)
    for unit in units:
        lines.append(f"  {str(unit.title).rjust(L)}: {unit.num_chars:6d} chars, {unit.num_questions:2d} questions, {unit.num_answers:2d} answers")

    return "\n".join(lines)


__all__ = [
    "get_summary",
]
