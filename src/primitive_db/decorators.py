import functools
import time

import prompt


def handle_db_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            print(f'Ошибка: Таблица "{args[1]}" не существует.')
            raise
        except ValueError as e:
            print(f'Ошибка: {e}.')
            raise
        except FileNotFoundError:
            print(f'Ошибка: Таблица "{args[0]}" не существует.')
            raise
        except Exception:
            print('Ошибка: что то пошло не так.')
            raise
    return wrapper


def confirm_action(action_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            answ = prompt.string(f'\n>>>Вы уверены, что хотите выполнить'
                                 f' "{action_name}"? [y/n]: ')
            if answ == 'y':
                return func(*args, **kwargs)
            print("Команда отменена")
        return wrapper
    return decorator


def log_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()

        execution_time = end_time - start_time
        print(f"Функция '{func.__name__}' выполнилась за {execution_time:.3f} сек.")
        return result
    return wrapper

