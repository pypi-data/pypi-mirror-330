assert __name__ == "__main__"

from ie_datasets.datasets.crossre.load import load_units


for domain in ("ai", "literature", "music", "news", "politics", "science"):
    for split in ("train", "dev", "test"):
        units = list(load_units(domain=domain, split=split))
        print(domain, split, len(units))

# TODO: summary
