from kombu import Queue, Exchange

from basicframe import settings


result_backend = settings.CELERY_RESULT_BACKEND
broker = settings.CELERY_BROKER_URL

task_default_queue = 'default'
task_default_exchange = 'tasks'
task_default_exchange_type = 'topic'
task_default_routing_key = 'task.default'


task_serializer = 'json'
accept_content = ['json']  # Ignore other content
result_serializer = 'json'
timezone = 'Asia/Shanghai'
enable_utc = True

# *（星号）：匹配一个关键字。
# #（井号）：匹配零个或多个关键字。
# .（点号）：用于分隔关键字。

news_processing_exchange = Exchange('news_processing_exchange', type='topic')
task_queues = (
    Queue('default', routing_key='task.#'),
    Queue('news_processing_queue', exchange=news_processing_exchange,routing_key='news_processing#'),
)

# task_routes = {
#     'tasks.add': 'low-priority',
#     'feed.tasks.*': {'queue': 'feeds'}
# }
#
# task_annotations = {
#     'tasks.add': {'rate_limit': '10/m'}
# }


# Example
# Say you have two servers, x, and y that handle regular tasks, and one server z
# that only handles feed related tasks, you can use this configuration:
# from kombu import Queue
#





# task_routes = ([
#     ('feed.tasks.*', {'queue': 'feeds'}),
#     ('web.tasks.*', {'queue': 'web'}),
#     (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
# ],)


# default queue name is celery You can change the name of the default queue by using the following configuration:
# app.conf.task_default_queue = 'default'

# You can specify as many queues as you want, so you can make this server process the default queue as well:
# celery -A proj worker -Q feeds,celery

# If you’re using RabbitMQ or Redis as the broker then you can also direct the workers to set a new rate limit for the task at runtime:
# celery -A tasks control rate_limit tasks.add 10/m

# now let us see how to create a queue. (as we know queue must have a exchange)
# A queue named “video” will be created with the following settings:
# {
#  'exchange': 'video',
#  'exchange_type': 'direct',
#  'routing_key': 'video
#  '}

# Special Routing Option
# app.conf.task_queues = [
#     Queue('tasks', Exchange('tasks'), routing_key='tasks',
#           queue_arguments={'x-max-priority': 10}),
# ]

# transport method
# app.conf.broker_transport_options = {
#     'queue_order_strategy': 'priority',
# }