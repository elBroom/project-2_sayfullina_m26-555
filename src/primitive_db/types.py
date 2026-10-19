VALID_TYPES = ('int', 'bool', 'str')

def convert_type(text: str) -> int|bool|str:
    """Конвертация строк в типы."""
    if text.isdigit():
        return int(text)
    if text.lower() in ('true', 'false'):
        return bool(text)
    if text.startswith('"'):
        return text.strip('"')
    return ""


def validate_type(_type, val):
	"""Валидация значений."""
	match _type:
		case 'int':
			if val.isdigit():
				return int(val)
		case 'bool':
			if val.lower() in ('true', 'false'):
				return bool(val)
		case 'str':
			if val.startswith('"'):
				return val.strip('"')
	return None
