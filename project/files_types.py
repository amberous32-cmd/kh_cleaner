from constants import SUFFIXES_TABLE

def classify(name: str) -> str | None:
    if "." not in name:
        return None

    suffix = name.split(".")[-1].lower()

    for folder, extensions in SUFFIXES_TABLE.items():
        if suffix in extensions:
            return folder

    return "Documents"