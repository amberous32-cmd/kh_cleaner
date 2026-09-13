import sys
import os
import json
import shutil
from pathlib import Path


CONFIG_NAME = "kh_cleaner.config.json"
APP_NAME = "kh_cleaner"

STANDARD_DIRECTORIES = ["Downloads", "Music", "Pictures", "Videos", "Documents"]
STANDARD_DIRECTORIES_RU = ["Загрузки", "Музыка", "Изображения", "Видео", "Документы"]

#Определяем место хранения папок конфигурации
def get_config_file() -> Path:
    if sys.platform == "win32":
        root = Path(os.environ.get("APPDATA") or (Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        root = Path.home() / "Library" / "Application Support"
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))

    config_dir = root / APP_NAME
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / CONFIG_NAME

#Определяем стандартные папки
def get_config_paths() -> dict:
    
    home = Path.home()
    
    # Сопоставляем только существующие стандартные папки
    detected_paths = {name: None for name in STANDARD_DIRECTORIES}

    #Проверяем, нашлись ли директории на английском языке
    for directory in home.iterdir():
        if directory.is_dir() and not directory.name.startswith('.') and directory.name in detected_paths:
            detected_paths[directory.name] = str(directory.resolve())

    #Проверяем, нашлись ли директории на русском языке
    detected_paths_ru = {name: None for name in STANDARD_DIRECTORIES_RU}
    for directory in home.iterdir():
        if directory.is_dir() and not directory.name.startswith('.') and directory.name in detected_paths_ru:
            detected_paths_ru[directory.name] = str(directory.resolve())

    #Если есть директории на русском языке, заменяем на них пути
    for foulder, path in detected_paths_ru.items():
        if path != None:
            if foulder == STANDARD_DIRECTORIES_RU[0]:
                detected_paths["Downloads"] = path
                
            if foulder == STANDARD_DIRECTORIES_RU[1]:
                detected_paths["Music"] = path

            if foulder == STANDARD_DIRECTORIES_RU[2]:
                detected_paths["Pictures"] = path

            if foulder == STANDARD_DIRECTORIES_RU[3]:
                detected_paths["Videos"] = path
        
            if foulder == STANDARD_DIRECTORIES_RU[4]:
                detected_paths["Documents"] = path


    config_file = get_config_file()

    # Если конфига нет — создаем
    if not config_file.exists():
        try:
            with open(config_file, "w", encoding='utf-8') as f:
                json.dump(detected_paths, f, indent=4, ensure_ascii=False)
                print("Файл конфигурации создан")
        except Exception as e:
            print(f"Ошибка при записи файла: {e}. Файл конфигурации будет удалён")
            config_file.unlink(missing_ok=True)
            raise e

    # Читаем конфиг
    with open(config_file, 'r', encoding="utf-8") as f:
        return json.load(f)

# Таблица расширений для сортировки по папкам
SUFFIXES_TABLE = {
    "Pictures": {
        "jpg", "jpeg", "png", "gif", "webp", "avif", "heic", "heif", "tiff", "tif", "bmp", 
        "ico", "svg", "eps", "ai", "cr2", "cr3", "nef", "arw", "dng", "raw", "psd"
    },
    "Music": {
        "mp3", "m4a", "aac", "ogg", "oga", "opus", "wma", "flac", "alac", "ape",
        "wav", "aif", "aiff", "mid", "midi", "amr", "m4r"
    },
    "Videos": {
        "mp4", "m4v", "mkv", "mov", "avi", "wmv", "webm", "flv", 
        "ts", "mts", "m2ts", "vob", "ogv", "3gp", "3g2", "mpeg", "mpg", "mpe", "asf", "rm", "swf"
    }
}

# Множество всех известных медиа-расширений для фильтрации документов
ALL_MEDIA_SUFFIXES = SUFFIXES_TABLE["Music"] | SUFFIXES_TABLE["Pictures"] | SUFFIXES_TABLE["Videos"]


def get_files_by_format(source_dir: Path, file_format: str) -> list[Path]:
    if not source_dir.exists():
        print(f"Папка источника {source_dir} не существует.")
        return []

    found_files = []
    for item in source_dir.iterdir():
        if not item.is_file():
            continue
            
        # Получаем расширение в нижнем регистре без точки
        ext = item.suffix.lstrip('.').lower()
        
        if file_format == "Documents":
            if ext not in ALL_MEDIA_SUFFIXES:
                found_files.append(item)
        elif file_format in SUFFIXES_TABLE:
            if ext in SUFFIXES_TABLE[file_format]:
                found_files.append(item)
                
    return found_files


def move_files_by_format(config: dict, file_format: str):
    if file_format not in STANDARD_DIRECTORIES:
        print(f"Ошибка: неизвестный формат {file_format}")
        return

    downloads_str = config.get("Downloads")
    target_dir_str = config.get(file_format)
    
    if not downloads_str or not target_dir_str:
        print(f"Целевая папка или Downloads для {file_format} не задана в конфиге. Пропуск.")
        return

    source_dir = Path(downloads_str)
    target_dir = Path(target_dir_str)
    
    # Создаем целевую папку, если её почему-то нет
    target_dir.mkdir(parents=True, exist_ok=True)

    files_to_move = get_files_by_format(source_dir, file_format)
    
    for file_path in files_to_move:
        dest_path = target_dir / file_path.name
        
        if not dest_path.exists():
            try:
                # shutil.move безопасен при переносе между разными дисками (C:\ -> D:\). Он нужен для кроссплатформерности на Windows
                shutil.move(str(file_path), str(dest_path))
                print(f"Перемещен: {file_path.name} -> {file_format}")
            except Exception as e:
                print(f"Не удалось переместить {file_path.name}: {e}")
        else:
            print(f"Файл {file_path.name} уже существует в {file_format}. Пропуск.")


def clean_downloads():
    config = get_config_paths()
    
    # Перемещаем файлы по всем категориям (кроме самой папки Downloads)
    categories = [cat for cat in STANDARD_DIRECTORIES if cat != "Downloads"]
    
    for category in categories:
        move_files_by_format(config, category)


if __name__ == "__main__":
    clean_downloads()
