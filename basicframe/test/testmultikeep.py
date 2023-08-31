import multiprocessing
import random
import time


def t_spider(index):
    # 这里代替你的爬虫启动逻辑
    print(f"Spider {index} started.")
    time.sleep(random.randint(0, 5))  # 模拟爬虫运行10秒
    print(f"Spider {index} finished.")


if __name__ == '__main__':
    num_cpus = multiprocessing.cpu_count()  # 获取CPU核心数量
    with multiprocessing.Pool(processes=num_cpus) as pool:
        # 创建足够多的任务，确保总是有8个爬虫运行
        pool.map(t_spider, range(100))  # 假设你有100个爬虫任务
    print("All spiders finished.")
