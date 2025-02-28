assert __name__ == "__main__"

from ie_datasets.datasets.knowledgenet.load import load_units


for split in ("train", "test-no-facts"):
    units = list(load_units(split=split))
    print(split, len(units))

# TODO: summary
