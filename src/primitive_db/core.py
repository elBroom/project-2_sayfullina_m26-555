def create_table(metadata: dict, table_name: str, columns: list) -> dict:
	"""Создание и валидация таблицы"."""
	if table_name in metadata:
		raise ValueError(f'Таблица "{table_name}" уже существует')

	has_id = False
	for column in columns:
		if 'ID:' in column:
			has_id = True
		valid_column(column)

	if not has_id:
		columns = ['ID:int'] + columns

	metadata[table_name] = columns
	print(f'Таблица "{table_name}" успешно создана со столбцами: {', '.join(columns)}')
	return metadata

def valid_column(column: str):
	"""Валидация таблицы."""
	val = column.split(':')
	if len(val) != 2:
		raise ValueError(f'Формат колонки "{column}" не поддерживается')

	if val[1] not in ('int', 'bool', 'str'):
		raise ValueError(f'Тип колонки "{val[1]}" не поддерживается')

def drop_table(metadata: dict, table_name: str) -> dict:
	"""Удаление таблицы."""
	try:
		del metadata[table_name]
		print(f'Таблица "{table_name}" успешно удалена.')
	except KeyError:
		raise ValueError(f'Таблица "{table_name}" не существует')
	
	return metadata


def list_tables(metadata: dict):
	"""Получение наличия таблиц."""
	for table_name in metadata.keys():
		print(f'- {table_name}')


def info_table(metadata: dict, table_name: str, cnt: int) -> dict:
	"""Получение информации таблицы."""
	try:
		print(f'Таблица: {table_name}')
		print(f'\nСтолбцы: {', '.join(metadata[table_name])}')
		print(f'\nКоличество записей: {cnt}')
	except KeyError:
		raise ValueError(f'Таблица "{table_name}" не существует')

	return metadata


def insert(metadata: dict, table_name: str, values: list) -> dict:
	"""Вставка в таблицу."""
	if table_name not in metadata:
		raise ValueError(f'Таблица "{table_name}" не существует')

	if len(values) != len(metadata[table_name]) - 1:
		raise ValueError('Количество переданных значений не равно количеству столбцов')

	# Валидирует типы данных для каждого значения в соответствии со схемой в metadata.
	# TODO
	# Генерирует новый ID (например, max(IDs) + 1 или len(data) + 1).
	# TODO
	# Добавляет новую запись (в виде словаря) в данные таблицы и возвращает их.
	return {}

def select(table_data: list, where_clause: dict=None) -> list:
	"""Получение данных таблицы."""
	if where_clause is None:
		return table_data

	key, val = where_clause.items()
	return [
		row for row in table_data if row[key] == val
	]


def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
	"""Обновление данных в таблице."""
	key, val = where_clause.items()

	for i, row in enumerate(table_data):
		if row[key] == val:
			for column, set_val in set_clause:
				row[i][column] = set_val

	return table_data

def delete(table_data: list, where_clause: dict):
	"""Удаление данных таблице."""
	key, val = where_clause.items()
	return [
		row for row in table_data if row[key] != val
	]
