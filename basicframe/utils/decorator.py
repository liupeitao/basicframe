import functools
import time

import requests
from tqdm import tqdm


def execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time:.5f} seconds to execute.")
        return result
    return wrapper


##
def log(func):
    def wrapper(*args, **kwargs):
        print(f"INFO: Running function {func.__name__} with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"INFO: Function {func.__name__} returned {result}")
        return result
    return wrapper


def exception_handler(exception_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exception_type as e:
                # 在这里处理指定类型的异常
                print(f"Exception occurred in {func.__name__}: {str(e)}")
        return wrapper
    return decorator


def request_with_progress(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        response = method(*args, **kwargs)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 4096  # 每次下载的数据块大小
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

        # 将原始响应包装为可迭代对象，以便在遍历过程中更新进度条
        response_iter = response.iter_content(block_size)

        # 更新进度条的同时获取响应内容
        response._content = b''
        for data in response_iter:
            progress_bar.update(len(data))
            response._content += data
        progress_bar.close()
        return response
    return wrapper


@request_with_progress
def make_request(url):
    return requests.get(url, stream=True)



def singleton(cls):
    """
    Singleton Decorator
    """
    instance = None
    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper