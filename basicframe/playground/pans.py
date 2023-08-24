import pandas as pd

# 加载Excel文件
file_path = '~/yingyuwenben.xlsx'
sheet_num = 3  # 0-based index, 所以第4个sheet是索引3

# 读取特定的sheet
df = pd.read_excel(file_path, sheet_name=sheet_num, header=None)

# 获取第25行之后的第三列的数据
# 注意: Pandas是基于0的索引，所以第25行是索引24，第三列是索引2
data = df.iloc[24:, 2]

# 将数据写入到文本文件中
with open('output.txt', 'w') as file:
    for item in data:
        file.write(str(item) + '\n')

print("Data written to output.txt.")
