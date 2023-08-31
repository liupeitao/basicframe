import multiprocessing
import random
import time

import subprocess
import multiprocessing
import time


def start_new_spider(index):
    print(f'start{index} spider')
    time.sleep(random.randint(10))

    print(f'end{index} spider')
def run_spiders(num_spiders=None, max_total_spiders=100):
    if num_spiders is None:
        num_spiders = multiprocessing.cpu_count()  # 默认使用CPU核心数量

    started_spiders = 0  # 已启动的爬虫数量
    processes = []

    # 启动初始爬虫
    for _ in range(num_spiders):
        if started_spiders < max_total_spiders:
            p = multiprocessing.Process(target=start_new_spider, args=(_,))
            p.start()
            processes.append(p)
            started_spiders += 1

    while started_spiders < max_total_spiders:
        # 检查每个进程，看它是否还在运行
        for index in range(len(processes)):
            if not processes[index].is_alive():
                # 如果进程不再运行，并且还没有达到历史最大任务数，则启动新的进程
                if started_spiders < max_total_spiders:
                    p = multiprocessing.Process(target=start_new_spider, args=(started_spiders,))
                    p.start()
                    processes[index] = p
                    started_spiders += 1
        time.sleep(5)  # 间隔5秒钟再次检查进程状态

    # 等待剩下的进程完成
    for p in processes:
        p.join()

    print("All tasks completed.")


if __name__ == '__main__':
    run_spiders()  # 你可以使用run_spiders(num_spiders=4, max_total_spiders=50)来调整参数
