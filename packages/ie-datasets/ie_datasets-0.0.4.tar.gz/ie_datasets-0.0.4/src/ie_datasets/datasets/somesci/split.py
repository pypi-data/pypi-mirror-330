"""
Adapted from dave-s477/SoMeNLP/bin/split_data
"""
import os
import random
import shutil
from typing import Literal, Sequence, TypeAlias

from math import ceil


SoMeSciSplit: TypeAlias = Literal["train", "devel", "test"]


def somesci_split(
        in_path: str,
        *,
        file_extension: str = ".txt",
        ratio: Sequence[int] = (60, 20, 20),
        set_names: Sequence[SoMeSciSplit] = ("train", "devel", "test"),
        seed: int = 2,
        move: bool = True,
):
    """
    Split corpus according to a specified ratio.
    in_path: Path to input dir. Subdirectories for each split will be created here.
    file_extension: Extension for recognizing unique files.
    ratio: Split ratio. Provided as int and has to sum to 100, e.g., 60 20 20
    set_names: Output set names for writing
    seed: The seed for random shuffling (default of 2 is hard-coded in SoMeSci)
    move: Move files instead of copying them (more efficient)
    """
    in_path = in_path.rstrip('/')

    if sum(ratio) != 100:
        raise RuntimeError(f"Input ratio {ratio} does not sum to 100")
    if len(ratio) != len(set_names):
        raise RuntimeError(f"Number of ratios and setnames has to match: {ratio} vs {set_names}")

    # glob is absurdly slow so we use listdir instead
    in_path_files = os.listdir(in_path)
    single_filenames = [f for f in in_path_files if f.endswith(file_extension)]
    all_files: list[list[str]] = []
    for filename in single_filenames:
        base_file_name = filename.removesuffix(file_extension)
        base_file_entries = [f for f in in_path_files if f.startswith(base_file_name)]
        all_files.append(base_file_entries)

    rng = random.Random(seed)
    rng.shuffle(all_files)

    cut_sum = 0
    prev_cut_idx = 0
    for cut, split_name in zip(ratio, set_names):
        cut_sum += cut
        cut_idx = ceil(len(all_files) * cut_sum / 100.0)
        split_path = os.path.join(in_path, split_name)
        os.makedirs(split_path, exist_ok=True)
        for files in all_files[prev_cut_idx:cut_idx]:
            for f in files:
                source_path = os.path.join(in_path, f)
                target_path = os.path.join(split_path, f)
                if move:
                    shutil.move(source_path, target_path)
                else:
                    shutil.copy(source_path, target_path)
        prev_cut_idx = cut_idx


__all__ = [
    "somesci_split",
    "SoMeSciSplit",
]
