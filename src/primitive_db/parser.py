import re
from typing import Tuple

re_value = r'\"\w+\"|\d+|true|false|True|False'
re_insert = r'insert into (\w+) values (\((?:(?:'+re_value+r'),? ?)+\))'
re_select = r'select from (\w+)( where (\w+) = ('+re_value+r'))?'
re_delete = r'delete from (\w+) where (\w+) = ('+re_value+r')'
re_update = r'update (\w+) set (\w+) = ('+re_value+r') where (\w+) = ('+re_value+r')'


def parse_insert(text: str) -> Tuple[str, list]:
    match = re.search(re_insert, text)
    if not match:
        raise ValueError('Формат запроса не поддерживается')
    return match.group(1), re.findall(re_value, match.group(2))


def parse_select(text: str) -> Tuple[str, dict|None]:
    match = re.search(re_select, text)
    if not match:
        raise ValueError('Формат запроса не поддерживается')
    # Условие where есть
    if match.group(2):
        return (
            match.group(1),
            {match.group(3).strip('"'): convert_type(match.group(4))}
        )
    return match.group(1), None


def parse_update(text: str) -> Tuple[str, dict, dict]:
    match = re.search(re_update, text)
    if not match:
        raise ValueError('Формат запроса не поддерживается')
    return (
        match.group(1),
        {match.group(2).strip('"'): convert_type(match.group(3))},
        {match.group(4).strip('"'): convert_type(match.group(5))},
    )


def parse_delete(text: str) -> Tuple[str, dict]:
    match = re.search(re_delete, text)
    if not match:
        raise ValueError('Формат запроса не поддерживается')
    return (
        match.group(1),
        {match.group(2).strip('"'): convert_type(match.group(3))},
    )

def convert_type(text: str) -> int|bool|str:
    if text.isdigit():
        return int(text)
    if text.lower() in ('true', 'false'):
        return bool(text)
    if text.startswith('"'):
        return text.strip('"')
    return ""