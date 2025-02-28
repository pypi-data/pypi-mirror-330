from typing import Iterable, Literal, TypeAlias

from datasets import load_dataset

from ie_datasets.datasets.hyperred.unit import HyperREDUnit
from ie_datasets.util.env import get_cache_dir


BASE_HYPERRED_DIR = get_cache_dir(subpath="hyperred")

HyperREDSplit: TypeAlias = Literal["train", "validation", "test"]


def load_units(split: HyperREDSplit) -> Iterable[HyperREDUnit]:
    dataset = load_dataset(
        path="declare-lab/HyperRED",
        split=split,
        cache_dir=BASE_HYPERRED_DIR,
    )
    for raw_unit in dataset:
        # strict mode causes an error when reading spans as tuples
        unit = HyperREDUnit.model_validate(raw_unit, strict=False)
        yield unit


__all__ = [
    "HyperREDSplit",
    "load_units",
]
