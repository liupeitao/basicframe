import redis
from basicframe.midwares.redisclient import RedisClient
redis_conn = RedisClient().connect()

# 打开文本文件并逐行读取内容
with open('../assets/tripage.txt', 'r') as file:
    lines = file.readlines()
    print(lines)
# 使用循环将每行内容存入 Redis
for line in lines:
    line = line.strip()  # 去掉行末的换行符或空格
    print(line)
    redis_conn.lpush('tripage', line)

print("Lines stored in Redis successfully!")