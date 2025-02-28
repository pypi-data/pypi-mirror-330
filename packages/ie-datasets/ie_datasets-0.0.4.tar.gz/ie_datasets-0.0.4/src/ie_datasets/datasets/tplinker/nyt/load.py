from ie_datasets.datasets.tplinker.load import (
    load_schema as load_tplinker_schema,
    load_units as load_tplinker_units,
    TPLinkerSplit,
)


def load_schema():
    return load_tplinker_schema(dataset="NYT")


def load_units(split: TPLinkerSplit):
    return load_tplinker_units(dataset="NYT", split=split)


__all__ = [
    "load_schema",
    "load_units",
]
