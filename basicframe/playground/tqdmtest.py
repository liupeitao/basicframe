from tqdm.auto import tqdm
import time

# 要添加进度条的函数
def process_data(data):
    for item in tqdm(data, desc="Processing"):
        # 模拟处理操作
        time.sleep(0.1)

# 示例数据列表
data = list(range(100))

# 调用带有进度条的函数
process_data(data)
