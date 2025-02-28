import json
import os
import shutil
from typing import Iterable, Literal, Mapping, TypeAlias

import gdown

from ie_datasets.datasets.tplinker.schema import TPLinkerRelationType, TPLinkerSchema
from ie_datasets.datasets.tplinker.unit import TPLinkerUnit
from ie_datasets.util.decompress import decompress_tar_gz
from ie_datasets.util.env import get_cache_dir


TPLinkerDatasetName: TypeAlias = Literal["NYT", "NYT*", "WebNLG", "WebNLG*"]
TPLinkerSplit: TypeAlias = Literal["train", "valid", "test"]

BASE_TPLINKER_DIR = get_cache_dir(subpath="tplinker")
GDRIVE_ID = "1RxBVMSTgBxhGyhaPEWPdtdX1aOmrUPBZ"
FILENAMES_BY_DATASET_AND_SPLIT: Mapping[TPLinkerDatasetName, tuple[str, Mapping[TPLinkerSplit, str]]] = {
    "NYT": ("nyt", {
        "train": "train_data.json",
        "valid": "valid_data.json",
        "test": "test_data.json",
    }),
    "NYT*": ("nyt_star", {
        "train": "train_data.json",
        "valid": "valid_data.json",
        "test": "test_triples.json",
    }),
    "WebNLG": ("webnlg", {
        "train": "train_data.json",
        "valid": "valid_data.json",
        "test": "test.json",
    }),
    "WebNLG*": ("webnlg_star", {
        "train": "train_data.json",
        "valid": "valid_data.json",
        "test": "test_triples.json",
    }),
}


def _download(gdrive_id: str = GDRIVE_ID):
    data_path = os.path.join(BASE_TPLINKER_DIR, "data4tplinker/data4bert")
    if not os.path.exists(data_path):
        tar_gz_path = os.path.join(BASE_TPLINKER_DIR, "tplinker.tar.gz")
        gdown.download(id=gdrive_id, output=tar_gz_path)
        decompress_tar_gz(tar_gz_path, BASE_TPLINKER_DIR)
        os.remove(tar_gz_path)
        shutil.rmtree(os.path.join(BASE_TPLINKER_DIR, "data4tplinker/data4bilstm"))
    return data_path


def load_schema(
        dataset: TPLinkerDatasetName,
) -> TPLinkerSchema:
    data_path = _download()
    dataset_dir, _ = FILENAMES_BY_DATASET_AND_SPLIT[dataset]

    with open(os.path.join(data_path, dataset_dir, "rel2id.json"), "r") as f:
        relation_to_id = json.load(f)
    assert isinstance(relation_to_id, dict)

    schema = TPLinkerSchema(relation_types=[
        TPLinkerRelationType(id=id, name=name)
        for name, id in relation_to_id.items()
    ])
    return schema


def load_units(
        dataset: TPLinkerDatasetName,
        split: TPLinkerSplit,
) -> Iterable[TPLinkerUnit]:
    schema = load_schema(dataset)

    data_path = _download()
    dataset_dir, filenames_by_split = FILENAMES_BY_DATASET_AND_SPLIT[dataset]
    filename = filenames_by_split[split]

    with open(os.path.join(data_path, dataset_dir, filename), "r") as f:
        units_json = json.load(f)

    for unit_json in units_json:
        unit = TPLinkerUnit.model_validate(unit_json)
        schema.validate_unit(unit)
        yield unit


__all__ = [
    "load_units",
    "TPLinkerDatasetName",
    "TPLinkerSplit",
]
