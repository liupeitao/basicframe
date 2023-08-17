import os

BOT_NAME = "basicframe"
RETRY_ENABLED = True
RETRY_TIMES: 1

SPIDER_MODULES = ["basicframe.spiders"]
NEWSPIDER_MODULE = "basicframe.spiders"

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 0.2

CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 100

COOKIES_ENABLED = False

TELNETCONSOLE_ENABLED = False

DOWNLOADER_MIDDLEWARES = {
    # "basicframe.middlewares.BasicframeDownloaderMiddleware": 543,
    "basicframe.middlewares.ProxyMiddleware": 300
}

ITEM_PIPELINES = {
    # "basicframe.pipelines.BasicframePipeline": 301,
    "basicframe.pipelines.articlespiderpipeline.ArticleSpiderPipeline": 301
}

REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'

REDIRECT_ENABLED = False
DOWNLOAD_TIMEOUT = 60

MAX_IDLE_TIME_BEFORE_CLOSE = 20

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

SCHEDULER = "scrapy_redis.scheduler.Scheduler"

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

import yaml

# 获取当前文件的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 根据当前文件的目录路径拼接配置文件的路径
config_file = os.path.join(current_dir, 'config.yaml')


def load_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


config = load_config(config_file)

REDIS_CONFIG = config['redis']
REDIS_URL = REDIS_CONFIG['url']

MYSQL_CONFIG = config['mysql']
MYSQL_HOST = MYSQL_CONFIG['host']
MYSQL_PORT = MYSQL_CONFIG['port']
MYSQL_DATABASE = MYSQL_CONFIG['database']
MYSQL_USERNAME = MYSQL_CONFIG['username']
MYSQL_PASSWORD = MYSQL_CONFIG['password']

CELERY_CONFIG = config['celery']
CELERY_BROKER_URL = CELERY_CONFIG['broker_url']
CELERY_RESULT_BACKEND = CELERY_CONFIG['result_backend']

rabbitmq_config = config['rabbitmq']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
RABBITMQ_USERNAME = rabbitmq_config['username']
RABBITMQ_PASSWORD = rabbitmq_config['password']
RABBITMQ_VIRTUAL_HOST = rabbitmq_config['virtual_host']

mongodb_config = config['mongodb']
MONGO_URL = mongodb_config['url']
MONGO_DB = mongodb_config['db']
MONGO_COLL = mongodb_config['coll']

logger_config = config['logger']
LOGGER_SAVE_DIR = logger_config['saved']
SCHEDULER_PERSIST = True
