import shlex

import prompt

from .constants import FILE_META
from .core import (
    create_table,
    delete,
    drop_table,
    info_table,
    insert,
    list_tables,
    select,
    update,
)
from .parser import parse_delete, parse_insert, parse_select, parse_update
from .utils import load_metadata, load_table_data, save_metadata, save_table_data


def run():
    """Запуск команды."""

    metadate = load_metadata(FILE_META)
    print_help()

    while True:
        user_input = prompt.string('\n>>>Введите команду: ')
        args = shlex.split(user_input)
        try:
            match args[0]:
                case 'create_table':
                    metadate = create_table(metadate, args[1], args[2:])
                    save_metadata(FILE_META, metadate)
                    save_table_data(args[1], [])
                case 'list_tables':
                    list_tables(metadate)
                case 'drop_table':
                    metadate = drop_table(metadate, args[1])
                    save_metadata(FILE_META, metadate)
                    save_table_data(args[1], [])
                case 'insert':
                    table, values = parse_insert(user_input)
                    table_data = load_table_data(table)
                    row = insert(metadate, table, values)
                    table_data.append(row)
                    save_table_data(table, table_data)
                case 'select':
                    table, where_clause = parse_select(user_input)
                    table_data = load_table_data(table)
                    select(table_data, where_clause)
                case 'update':
                    table, set_clause, where_clause = parse_update(user_input)
                    table_data = load_table_data(table)
                    table_data = update(table_data, set_clause, where_clause)
                    save_table_data(table, table_data)
                case 'delete':
                    table, where_clause = parse_delete(user_input)
                    table_data = load_table_data(table)
                    table_data = delete(table_data, where_clause)
                    save_table_data(table, table_data)
                case 'info':
                    cnt = len(load_table_data(args[1]))
                    info_table(metadate, args[1], cnt)
                case 'exit':
                    break
                case 'help':
                    print_help()
                case _:
                    print(f'Функции {args[0]} нет. Попробуйте снова.')
        except Exception:
            pass


def print_help():
    """Получение информации о командах."""
   
    print('Функции:')
    print('<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу')
    print('<command> list_tables - показать список всех таблиц')
    print('<command> drop_table <имя_таблицы> - удалить таблицу')

    print('<command> insert into <имя_таблицы> values '
          '(<значение1>, <значение2>, ...) - создать запись.')
    print('<command> select from <имя_таблицы> '
          'where <столбец> = <значение> - прочитать записи по условию.')
    print('<command> select from <имя_таблицы> - прочитать все записи.')
    print('<command> update <имя_таблицы> set <столбец1> = <новое_значение1>'
          ' where <столбец_условия> = <значение_условия> - обновить запись.')
    print('<command> delete from <имя_таблицы> '
          'where <столбец> = <значение> - удалить запись.')
    print('<command> info <имя_таблицы> - вывести информацию о таблице.')

    print('\nОбщие команды:')
    print('<command> exit - выход из программы')
    print('<command> help - справочная информация\n')
