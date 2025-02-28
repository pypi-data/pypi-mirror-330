import json
import os
from typing import Iterable, Literal, TypeAlias

from ie_datasets.datasets.docred.load import load_schema
from ie_datasets.datasets.docred.unit import DocREDUnit
from ie_datasets.util.env import get_cache_dir
from ie_datasets.util.wget import open_or_wget


ReDocREDSplit: TypeAlias = Literal["train", "dev", "test"]


BASE_REDOCRED_DIR = get_cache_dir(subpath="re_docred")
DATASET_BASE_URL = "https://raw.githubusercontent.com/tonytan48/Re-DocRED/refs/heads/main/data"


def load_units(
        split: ReDocREDSplit,
        dataset_base_url: str = DATASET_BASE_URL,
) -> Iterable[DocREDUnit]:
    split_path = os.path.join(BASE_REDOCRED_DIR, f"{split}.jsonl")

    if os.path.exists(split_path):
        with open(split_path, "r") as f:
            for line in f:
                unit = DocREDUnit.model_validate_json(line, strict=True)
                assert unit.is_labelled
                yield unit

    else:
        units: list[DocREDUnit] = []

        with open_or_wget(
            url=f"{dataset_base_url}/{split}_revised.json",
            local_path=os.path.join(BASE_REDOCRED_DIR, f"raw/{split}_revised.json"),
        ) as f:
            units_json = json.load(f)
            assert isinstance(units_json, list)

        for unit_json in units_json:
            assert isinstance(unit_json, dict)
            entities = unit_json.pop("vertexSet")
            for entity_mentions in entities:
                for mention in entity_mentions:
                    assert isinstance(mention, dict)
                    mention["entity_type"] = mention.pop("type")
                    mention.pop("global_pos")
                    mention.pop("index")

            unit_json["vertex_set"] = entities
            unit = DocREDUnit.model_validate_json(json.dumps(unit_json), strict=True)
            assert unit.is_labelled
            units.append(unit)

        with open(split_path, "x") as f:
            for unit in units:
                f.write(unit.model_dump_json() + "\n")

        yield from units


__all__ = [
    "load_schema",
    "load_units",
    "ReDocREDSplit",
]
