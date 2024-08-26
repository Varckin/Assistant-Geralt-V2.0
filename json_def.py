import json


def json_read(file_name: str):
        with open(file_name, 'r', encoding='utf-8') as file:
            data: dict = json.load(file)
            return data