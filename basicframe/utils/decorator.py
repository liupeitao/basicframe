import time


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
