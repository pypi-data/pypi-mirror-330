import sys
import threading
import time

import cachetools


def func_cache_ignore_args(ttl=sys.maxsize):
    cache = cachetools.TTLCache(maxsize=99999, ttl=ttl)
    lock = threading.Lock()

    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            key = func.__name__
            if key in cache:
                try:
                    return cache[key]
                except KeyError:
                    pass
            with lock:
                try:
                    return cache[key]
                except KeyError:
                    pass
                result = func(*args, **kwargs)
                cache[key] = result
            return result

        return wrapper

    return actual_decorator


# 定义支持自定义ttl的缓存装饰器
def cache_with_custom_time(ttl=sys.maxsize):
    cache = cachetools.TTLCache(maxsize=99999, ttl=ttl)
    lock = threading.Lock()

    def actual_decorator(func):
        def wrapper(*args, **kwargs):
            key = args + tuple(kwargs.items())
            if key in cache:
                try:
                    return cache[key]
                except KeyError:
                    pass
            with lock:
                try:
                    return cache[key]
                except KeyError:
                    pass
                result = func(*args, **kwargs)
                cache[key] = result
            return result

        return wrapper

    return actual_decorator


# 示例函数，这里只是简单的数学运算，你可以替换成任何复杂的函数
@func_cache_ignore_args()  # 设置缓存有效期为150ms，可按需修改
def my_function(x, y=1):
    print(f"Calculating... for args: {x}, {y}")
    return (x + y) * 2


# 测试多线程并发情况的函数
def test_concurrency():
    threads = []
    for _ in range(10):
        t = threading.Thread(target=lambda: print(my_function(2, 3)))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    for i in range(1000):
        my_function(2, 3)
        time.sleep(0.05)
        print('-----')
    # print(my_function(2, 3))
    # print(my_function(2, 3))
    # time.sleep(0.2)
    # print(my_function(2, 3))
    # print("Testing concurrency:")
    # test_concurrency()
