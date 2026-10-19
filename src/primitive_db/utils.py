import json
import os

from .constants import DIR_DATA
from .decorators import handle_db_errors


def load_metadata(filepath: str):
    """ Загружает DDL из файла."""
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@handle_db_errors
def save_metadata(filepath: str, data: dict):
    """ Загружает DDL в файл."""
    with open(filepath, 'w+') as f:
        json.dump(data, f)

@handle_db_errors
def load_table_data(table_name: str) -> list:
    """ Загружает данные таблицы из файла."""
    os.makedirs(DIR_DATA, exist_ok=True)
    with open(os.path.join(DIR_DATA, table_name+'.json')) as f:
        return json.load(f)

@handle_db_errors
def save_table_data(table_name: str, data: list):
    """ Загружает данные таблицы в файл."""
    os.makedirs(DIR_DATA, exist_ok=True)
    with open(os.path.join(DIR_DATA, table_name+'.json'), 'w+') as f:
        json.dump(data, f)
