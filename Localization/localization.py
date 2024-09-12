from json_def import json_read
from pathlib import Path


def getStr(lang_code: str, key_str: str) -> str:
    if Path(f"{str(Path.cwd())}/Localization/{lang_code}.json").is_file():
        localization: dict = json_read(f"{str(Path.cwd())}/Localization/{lang_code}.json")
        return localization.get(key_str)
    else:
        localization: dict = json_read(f"{str(Path.cwd())}/Localization/en.json")
        return localization.get(key_str)
