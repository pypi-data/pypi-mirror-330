import os
from typing import Iterable, Literal, TypeAlias

from ie_datasets.datasets.knowledgenet.unit import KnowledgeNetUnit
from ie_datasets.util.env import get_cache_dir
from ie_datasets.util.wget import open_or_wget


KnowledgeNetSplit: TypeAlias = Literal[
    "train",
    "test-no-facts",
]

BASE_CROSSRE_PATH = get_cache_dir(subpath="crossre")
BASE_DATA_URL = "https://raw.githubusercontent.com/diffbot/knowledge-net/refs/heads/master/dataset"


def load_units(
        split: KnowledgeNetSplit,
) -> Iterable[KnowledgeNetUnit]:
    split_path = os.path.join(BASE_CROSSRE_PATH, f"{split}.jsonl")
    data_url = f"{BASE_DATA_URL}/{split}.json"
    with open_or_wget(split_path, data_url) as f:
        for line in f:
            unit = KnowledgeNetUnit.model_validate_json(line)
            if split == "test-no-facts":
                assert unit.num_facts == 0
            yield unit


__all__ = [
    "load_units",
    "KnowledgeNetSplit",
]
