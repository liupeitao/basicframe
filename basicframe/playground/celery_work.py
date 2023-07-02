from tasks import app

# 启动Celery Worker进程
if __name__ == '__main__':
    app.worker_main(['-A', 'duration', '-l', 'info'])
