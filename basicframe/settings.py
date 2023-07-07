# Scrapy settings for basicframe project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = "basicframe"

# BOT_NAME = "articlex_spider"

SPIDER_MODULES = ["basicframe.spiders"]
NEWSPIDER_MODULE = "basicframe.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "basicframe (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "basicframe.middlewares.BasicframeSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "basicframe.middlewares.BasicframeDownloaderMiddleware": 543,
    "basicframe.middlewares.ProxyMiddleware": 300
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # "basicframe.pipelines.BasicframePipeline": 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# scrapy -redis article
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

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
REDIS_HOST = REDIS_CONFIG['host']
REDIS_PORT = REDIS_CONFIG['port']
REDIS_DB = REDIS_CONFIG['db']
REDIS_PASSWORD = REDIS_CONFIG['password']
REDIS_URL = REDIS_CONFIG['url']

# 获取MySQL配置
MYSQL_CONFIG = config['mysql']
MYSQL_HOST = MYSQL_CONFIG['host']
MYSQL_PORT = MYSQL_CONFIG['port']
MYSQL_DATABASE = MYSQL_CONFIG['database']
MYSQL_USERNAME = MYSQL_CONFIG['username']
MYSQL_PASSWORD = MYSQL_CONFIG['password']

# 获取MongoDB配置
MONGODB_CONFIG = config['mongodb']
MONGODB_HOST = MONGODB_CONFIG['host']
MONGODB_PORT = MONGODB_CONFIG['port']
MONGODB_DATABASE = MONGODB_CONFIG['database']

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
MONGODB_HOST = mongodb_config['host']
MONGODB_PORT = mongodb_config['port']
MONGO_DB = mongodb_config['db']
MONGO_URL = mongodb_config['url']
MONGO_COLL = mongodb_config['coll']

