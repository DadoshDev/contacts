import logging
from typing import Callable

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s - %(filename)s',
    datefmt="%Y-%m-%d %H:%M:%",
    filename='logs.log'
)


def logger(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            func_res = func(*args, **kwargs)
            message = (f"Function: {func.__name__} Result: {func_res}"
                       f" - Arguments: {args}, {kwargs}")
            logging.info(message)
            return func_res
        except Exception as e:
            message = f"Function: {func.__name__} Error: {e}"
            logging.error(message)
            raise

    return wrapper
