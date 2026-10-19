from prettytable import PrettyTable

from .decorators import confirm_action, handle_db_errors, log_time
from .utils import load_table_data


@handle_db_errors
def create_table(metadata: dict, table_name: str, columns: list) -> dict:
	"""Создание и валидация таблицы."""
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

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata: dict, table_name: str) -> dict:
	"""Удаление таблицы."""
	del metadata[table_name]
	print(f'Таблица "{table_name}" успешно удалена.')
	
	return metadata

def list_tables(metadata: dict):
	"""Получение наличия таблиц."""
	for table_name in metadata.keys():
		print(f'- {table_name}')

@handle_db_errors
def info_table(metadata: dict, table_name: str, cnt: int) -> dict:
	"""Получение информации таблицы."""
	columns = metadata[table_name]

	print(f'Таблица: {table_name}')
	print(f'Столбцы: {', '.join(columns)}')
	print(f'Количество записей: {cnt}')

	return metadata

@handle_db_errors
@log_time
def insert(metadata: dict, table_name: str, values: list) -> dict:
	"""Вставка в таблицу."""
	if len(values) != len(metadata[table_name]) - 1:
		raise ValueError('Количество переданных значений не равно количеству столбцов')

	data = {"ID": load_last_id(table_name) + 1}
	# Валидирует типы данных для каждого значения в соответствии со схемой в metadata.
	for column, val in zip(metadata[table_name][1:], values):
		name, _type = column.split(':')
		data[name] = validate_value(_type, val)
		if data[name] is None:
			raise ValueError(f"Для колонки {name} ожидается тип {_type}")

	print(f'Запись с ID={data["ID"]} успешно добавлена в таблицу "{table_name}".')
	return data

@log_time
def select(table_data: list, where_clause: dict|None=None):
	"""Получение данных таблицы."""
	if where_clause is None:
		rows = [
			row.values() for row in table_data
		]
	else:
		key, val = next(iter(where_clause.items()))
		rows = [
			row.values() for row in table_data if row[key] == val
		]

	if len(rows) == 0:
		print("Нет данных")
		return

	table = PrettyTable()
	table.field_names = list(table_data[0].keys())
	table.add_rows(rows)
	print(table)


def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
	"""Обновление данных в таблице."""
	key, val = next(iter(where_clause.items()))

	find_idx = None
	for i, row in enumerate(table_data):
		if row[key] == val:
			find_idx = i
			break

	if find_idx is not None:
		key, val = next(iter(set_clause.items()))
		table_data[find_idx][key] = val

		print(f'Запись с ID={table_data[find_idx]["ID"]} успешно обновлена.')
	else:
		raise ValueError(f'Запись с условием {key} = {val} не существует')
	return table_data

@confirm_action("удаление записи")
def delete(table_data: list, where_clause: dict):
	"""Удаление данных таблице."""
	key, val = next(iter(where_clause.items()))
	last_id = None

	new_rows = []
	for row in table_data:
		if row[key] == val:
			last_id = row["ID"]
		else:
			new_rows.append(row)

	if last_id:
		print(f'Запись с ID={last_id} успешно удалена.')
	else:
		print(f'Запись с условием {key} = {val} не существует')

	return new_rows

def load_last_id(table_name: str) -> int:
	"""Получение последнего ID."""
	data = load_table_data(table_name)
	if len(data) == 0:
		return 0
	return data[len(data) - 1]["ID"]

def validate_value(_type, val):
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
