from pathlib import Path
from constants import APP_NAME, STANDARD_DIRECTORIES, STANDARD_DIRECTORIES_RU, RU_ENG_DICT, CONFIG_NAME
import sys, os, json

def get_config_dir() -> Path:

    platform = sys.platform

    if platform == "win32":
        root = Path(os.environ.get("APPDATA") or Path.home() / "AppData" / "Roaming")
    elif platform == "darwin":
        root = Path(Path.home() / "Library" / "Application Support")
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home()/ ".config")

    return root / APP_NAME

def detect_standard_dirs() -> dict:
    home = Path.home()
    paths = {i: None for i in STANDARD_DIRECTORIES}

    for folder in STANDARD_DIRECTORIES:
        path = home / folder
        if path.exists():
            paths[folder] = str(path)

    #Папки на ru приоритетней папок на eng
    for folder in STANDARD_DIRECTORIES_RU:
            path = home / folder
            if path.exists():
                paths[RU_ENG_DICT[folder]] = str(path)
    return paths


def load_config() -> dict:
    root = get_config_dir()
    root.parent.mkdir(parents=True, exist_ok=True)
    if not root.exists():
        with open(root, "w", encoding="utf-8") as f:
            detected_paths = detect_standard_dirs()
            json.dump(detected_paths, f, indent=4, ensure_ascii=False)
            print("Configuration file is created")
            return detected_paths
    else:
        with open(root / CONFIG_NAME, "r", encoding="utf-8") as f:
             return json.load(f)
        
def save_config(cfg: dict) -> None:
    root = get_config_dir() / CONFIG_NAME
    with open(root, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)

print(detect_standard_dirs())