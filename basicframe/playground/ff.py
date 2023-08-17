import time
import matplotlib.pyplot as plt
import requests
from functools import partial
from basicframe.spiders.extractors.articelextractor import extractor_articel


def measure_execution_time(func, num_repeats):
    execution_times = []

    for _ in range(num_repeats):
        start_time = time.time()
        result = func()
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)

    return execution_times


def generate_time_plot(func, num_repeats):
    execution_times = measure_execution_time(func, num_repeats)
    print(execution_times)
    plt.plot(execution_times, marker='o')
    plt.xlabel('Execution Number')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time of function')
    plt.show()


if __name__ == '__main__':
    response = requests.get('http://www.naewoeilbo.com/news/articleView.html?idxno=780771')
    site_info = {'domain': 'ss'}
    num_repeats = 30

    # 将extractor_articel函数和参数封装为可调用的函数
    func_to_measure = partial(extractor_articel, response, site_info)

    generate_time_plot(func_to_measure, num_repeats)
