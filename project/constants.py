#Названия конфига и самого приложения
CONFIG_NAME = "kh_cleaner.config.json"
APP_NAME = "kh_cleaner"


#Стандартные папкиы
STANDARD_DIRECTORIES = ["Downloads", "Music", "Pictures", "Videos", "Documents"]
STANDARD_DIRECTORIES_RU = ["Загрузки", "Музыка", "Изображения", "Видео", "Документы"]
RU_ENG_DICT = {"Музыка": "Music", "Изображения": "Pictures", "Видео": "Video", "Документы": "Documents", "Загрузки": "Downloads"}

#Стандартная связка тип файла - расширения
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