import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata

FILE = 'db_meta.json'

def run():
    metadate = load_metadata(FILE)
    print_help()

    while True:
        user_input = prompt.string('\n>>>Введите команду: ')
        args = shlex.split(user_input)
        try:
            match args[0]:
                case 'create_table':
                    metadate = create_table(metadate, args[1], args[2:])
                    save_metadata(FILE, metadate)
                case 'list_tables':
                    list_tables(metadate)
                case 'drop_table':
                    metadate = drop_table(metadate, args[1])
                    save_metadata(FILE, metadate)
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
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 
