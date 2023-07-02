from celery import Celery
import basicframe.settings as settings
# 创建 Celery 应用
app = Celery('myapp', broker=settings.CELERY_BROKER_URL)
# 配置 Celery
app.conf.update(
    result_backend=settings.CELERY_BROKER_URL,  # Redis URL
    # 其他配置参数...
)


if __name__ == '__main__':
    app.start()


# cli启动命令
# celery -A celery_app worker --loglevel=info