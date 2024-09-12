import json


def json_read(file_name: str) -> dict:
        with open(file_name, 'r', encoding='utf-8') as file:
            data: dict = json.load(file)
            return data


def json_write(file_name: str, dict: dict):
    with open(file_name, "w", encoding='utf-8') as file:
        json.dump(dict, file, ensure_ascii=False, indent=4)
