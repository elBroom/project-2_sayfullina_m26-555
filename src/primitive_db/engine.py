import shlex

import prompt

from .constants import FILE_META
from .core import (
    create_table,
    drop_table,
    info_table,
    insert,
    list_tables,
    select,
    update,
)
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
                case 'list_tables':
                    list_tables(metadate)
                case 'drop_table':
                    metadate = drop_table(metadate, args[1])
                    save_metadata(FILE_META, metadate)
                case 'insert':
                    table_data = load_table_data(args[1])
                    row = insert(metadate, args[1], args[2:])
                    table_data.append(row)
                    save_table_data(args[1], table_data)
                case 'select':
                    # TODO parse where
                    where_clause = None
                    table_data = load_table_data(args[1])
                    select(table_data, where_clause)
                    save_table_data(args[1], table_data)
                case 'update':
                    # TODO parse set_clause
                    set_clause = {}
                    # TODO parse where
                    where_clause = {}
                    table_data = load_table_data(args[1])
                    table_data = update(table_data, set_clause, where_clause)
                    save_table_data(args[1], table_data)
                case 'info':
                    cnt = len(load_table_data(args[1]))
                    info_table(metadate, args[1], cnt)
                case 'exit':
                    break
                case 'help':
                    print_help()
                case _:
                    print(f'Функции {args[0]} нет. Попробуйте снова.')
        except IndexError:
            print(f'Некорректное значение: {user_input}. Попробуйте снова.')
        except ValueError as e:
            print(f'Ошибка: {e}.')



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
