from functools import cached_property
from typing import Sequence

from ie_datasets.util.interfaces import ImmutableModel


class CrossREEntity(ImmutableModel):
    start: int
    end: int
    entity_type: str


class CrossRERelation(ImmutableModel):
    head_start: int
    head_end: int
    tail_start: int
    tail_end: int
    relation_type: str
    explanation: str
    uncertain: bool
    syntax_ambiguity: bool


class CrossREUnit(ImmutableModel):
    doc_key: str
    sentence: Sequence[str]
    ner: Sequence[tuple[int, int, str]]
    relations: Sequence[tuple[int, int, int, int, str, str, bool, bool]]

    @cached_property
    def entity_objects(self) -> Sequence[CrossREEntity]:
        return [
            CrossREEntity(
                start=start,
                end=end,
                entity_type=entity_type,
            )
            for start, end, entity_type in self.ner
        ]

    @cached_property
    def relation_objects(self) -> Sequence[CrossRERelation]:
        return [
            CrossRERelation(
                head_start=head_start,
                head_end=head_end,
                tail_start=tail_start,
                tail_end=tail_end,
                relation_type=relation_type,
                explanation=explanation,
                uncertain=uncertain,
                syntax_ambiguity=syntax_ambiguity,
            )
            for (
                head_start,
                head_end,
                tail_start,
                tail_end,
                relation_type,
                explanation,
                uncertain,
                syntax_ambiguity,
            ) in self.relations
        ]


__all__ = [
    "CrossREEntity",
    "CrossRERelation",
    "CrossREUnit",
]
