from typing import Sequence

from ie_datasets.util.interfaces import ImmutableModel


class DocREDRelationType(ImmutableModel):
    id: str
    description: str


class DocREDSchema(ImmutableModel):
    relation_types: Sequence[DocREDRelationType]


__all__ = [
    "DocREDRelationType",
    "DocREDSchema",
]
