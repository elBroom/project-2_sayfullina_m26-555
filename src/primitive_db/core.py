def create_table(metadata: dict, table_name: str, columns: list) -> dict:
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
	val = column.split(':')
	if len(val) != 2:
		raise ValueError(f'Формат колонки "{column}" не поддерживается')

	if val[1] not in ('int', 'bool', 'str'):
		raise ValueError(f'Тип колонки "{val[1]}" не поддерживается')

def drop_table(metadata: dict, table_name: str) -> dict:
	try:
		del metadata[table_name]
		print(f'Таблица "{table_name}" успешно удалена.')
	except KeyError:
		raise ValueError(f'Таблица "{table_name}" не существует')
	
	return metadata


def list_tables(metadata: dict):
	for table_name in metadata.keys():
		print(f'- {table_name}')
