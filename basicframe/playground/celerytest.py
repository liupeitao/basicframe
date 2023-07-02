from tasks import get_m3u8_duration_task, down_m3u8_task
for i in range(1000):
    result = get_m3u8_duration_task.delay('https://v5.cdtlas.com/20220619/6hCH3rE1/index.m3u8', i)
    print(result.id)



# 1 run command `celery -A tasks worker --loglevel=info` in cli
# 2 run this py file