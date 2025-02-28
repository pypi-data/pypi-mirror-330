from functools import cached_property
from typing import Literal, Mapping, Sequence, TypeAlias

from pydantic import model_validator

from ie_datasets.util.interfaces import ImmutableModel


ChemProtEntityType: TypeAlias = Literal[
    "CHEMICAL",
    "GENE-N",
    "GENE-Y",
]

ChemProtRelationType: TypeAlias = Literal[
    "CPR:0",
    "CPR:1",
    "CPR:2",
    "CPR:3",
    "CPR:4",
    "CPR:5",
    "CPR:6",
    "CPR:7",
    "CPR:8",
    "CPR:9",
    "CPR:10",
]


class ChemProtEntityMention(ImmutableModel):
    id: str
    entity_type: ChemProtEntityType
    text: str
    start: int
    end: int


class ChemProtRelation(ImmutableModel):
    relation_type: ChemProtRelationType
    argument_1: str
    argument_2: str


class ChemProtUnit(ImmutableModel):
    pmid: int
    text: str
    entities: Sequence[ChemProtEntityMention]
    relations: Sequence[ChemProtRelation]

    @property
    def num_chars(self) -> int:
        return len(self.text)

    @property
    def num_entity_mentions(self) -> int:
        return len(self.entities)

    @property
    def num_relations(self) -> int:
        return len(self.relations)

    @cached_property
    def entities_by_id(self) -> Mapping[str, ChemProtEntityMention]:
        entities_by_id = {entity.id: entity for entity in self.entities}
        assert len(entities_by_id) == self.num_entity_mentions
        return entities_by_id

    @model_validator(mode="after")
    def validate_entities(self):
        for entity in self.entities:
            assert self.text[entity.start:entity.end] == entity.text
        return self

    @model_validator(mode="after")
    def validate_relations(self):
        for relation in self.relations:
            assert relation.argument_1 in self.entities_by_id
            assert relation.argument_2 in self.entities_by_id
        return self


__all__ = [
    "ChemProtEntityMention",
    "ChemProtEntityType",
    "ChemProtRelation",
    "ChemProtRelationType",
    "ChemProtUnit",
]
