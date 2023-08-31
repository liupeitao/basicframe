import requests


from basicframe.spiders.extractors.articelextractor import extractor_articel, newspaper_extractor, gne_extractor, goose_extractor

response = requests.get('http://www.naewoeilbo.com/news/articleView.html?idxno=780771')

import time


def measure_execution_time(num_repeats):
    def decorator(func):
        def wrapper(*args, **kwargs):
            total_time = 0
            for _ in range(num_repeats):
                start_time = time.time()
                func(*args, **kwargs)
                end_time = time.time()
                total_time += end_time - start_time
            print(
                f"Function '{func.__name__}' total execution time for {num_repeats} repeats: {total_time:.6f} seconds")
            return total_time

        return wrapper

    return decorator


@measure_execution_time(num_repeats=200)
def test_extractor_articel():
    item = extractor_articel(response)
    print(item)
    assert item is not None


@measure_execution_time(num_repeats=100)
def test_newspaper_extractor():
    newspaper_extractor(response.text)

@measure_execution_time(num_repeats=100)
def test_gne_extractor():
    gne_extractor(response.text)

@measure_execution_time(num_repeats=100)
def test_goose_extractor():
    goose_extractor(response.text)




