import os

BOT_NAME = "basicframe"
RETRY_ENABLED = True
RETRY_TIMES: 1

SPIDER_MODULES = ["basicframe.spiders"]
NEWSPIDER_MODULE = "basicframe.spiders"



# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False




DOWNLOADER_MIDDLEWARES = {
    # "basicframe.middlewares.BasicframeDownloaderMiddleware": 543,
    "basicframe.middlewares.ProxyMiddleware": 300
}


ITEM_PIPELINES = {
    # "basicframe.pipelines.BasicframePipeline": 301,
    "basicframe.pipelines.articlespiderpipeline.ArticleSpiderPipeline": 301
}
REDIRECT_ENABLED = True

REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'


DOWNLOAD_TIMEOUT = 60

MAX_IDLE_TIME_BEFORE_CLOSE = 20

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# scrapy -redis article
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# 使用 Redis 的去重过滤器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 解析yaml文件配置
import yaml



# 获取当前文件的目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 根据当前文件的目录路径拼接配置文件的路径
config_file = os.path.join(current_dir, 'config.yaml')


def load_config(file_path):
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


# 导入配置
config = load_config(config_file)

# 获取Redis配置
# 获取Redis配置
REDIS_CONFIG = config['redis']
REDIS_URL = REDIS_CONFIG['url']
REDIS_URL_MUL = REDIS_CONFIG['url_mul']

# 获取MySQL配置
MYSQL_CONFIG = config['mysql']
MYSQL_HOST = MYSQL_CONFIG['host']
MYSQL_PORT = MYSQL_CONFIG['port']
MYSQL_DATABASE = MYSQL_CONFIG['database']
MYSQL_USERNAME = MYSQL_CONFIG['username']
MYSQL_PASSWORD = MYSQL_CONFIG['password']

# 获取Celery配置
CELERY_CONFIG = config['celery']
CELERY_BROKER_URL = CELERY_CONFIG['broker_url']
CELERY_RESULT_BACKEND = CELERY_CONFIG['result_backend']
# 其他Celery配置参数...

# 获取RabbitMQ配置
rabbitmq_config = config['rabbitmq']
RABBITMQ_HOST = rabbitmq_config['host']
RABBITMQ_PORT = rabbitmq_config['port']
RABBITMQ_USERNAME = rabbitmq_config['username']
RABBITMQ_PASSWORD = rabbitmq_config['password']
RABBITMQ_VIRTUAL_HOST = rabbitmq_config['virtual_host']

# mongodb 配置
mongodb_config = config['mongodb']
MONGO_URL = mongodb_config['url']
MONGO_DB = mongodb_config['db']
MONGO_DB_MUL = mongodb_config['db_mul']
MONGO_COLL = mongodb_config['coll']
MONGO_COLL_SITEINFO = mongodb_config['coll_siteinfo']
# logger 配置
logger_config = config['logger']
LOGGER_SAVE_DIR = logger_config['saved']
SCHEDULER_PERSIST = True  #将程序持久化保存