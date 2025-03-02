import functools


def singleton(func):
    @functools.lru_cache(maxsize=1)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

# @singleton
# def my_function():
#     print("函数执行")
#     return 42
