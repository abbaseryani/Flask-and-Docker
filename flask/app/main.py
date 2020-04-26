from flask import Flask
from celery import Celery
from .celery_example import make_celery
from kombu import Queue, Exchange
from datetime import timedelta
import logging

logging.basicConfig(level=logging.INFO,
                    format= '%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
#celery = Celery(broker='redis://localhost:6379/0')
app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = 'redis://localhost:6379/0'
app.config["CELERY_BACKEND"] = 'redis://localhost:6379/1'

app.config['CELERY_QUEUES'] = (
    Queue('reverse_q', Exchange('reverse_q'), routing_key='reverse_q'),
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('processing', Exchange('processing'), routing_key='processing')
)

# app.config['CELERY_ROUTES'] = {
#     'main.reverse': {'queue': 'reverse_q', 'routing_key': 'reverse_q'},
#     'main.reverse': {'queue': 'default', 'routing_key': 'default'},
#     'app.tasks.update_files_from_search': {'queue': 'fast', 'routing_key': 'fast'},
# }

app.config['CELERY_ROUTES'] = {
    'main.reverse': {
        'exchange': 'reverse_q',
        'exchange_type': 'direct',
        'routing_key': 'reverse_q'
    },
    'main.cooling': {
        'exchange': 'default',
        'exchange_type': 'direct',
        'routing_key': 'default'
    }
}

app.config['CELERYBEAT_SCHEDULE']= {
    'reverseTask': {
        'task': 'main.reverse',
        'schedule': timedelta(seconds=10),
        'options': {'queue' : 'reverse_q'}
    }
}
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#         'task': 'tasks.add',
#         'schedule': timedelta(seconds=10)
#     },
# }

#celery = make_celery(app)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route("/")
def home():
    return "Hello, World!"

@app.route('/process/<names>')
def process(names):
    reverse.delay(names)
    return "This should be processed with reverse_q"

@app.route('/update/<names>')
def update(names):
    cooling.delay(names)
    return "This should be processed with default"

#@celery.task(name='celery_example.reverse')
@celery.task
def reverse():
    print('Start reverse function -------------------------------')
    #return wort[::-1]
    return "Abbas"


@celery.task
def cooling(wort):
    return wort[::-1]

@celery.task
def trash(wort):
    return wort[::-1]
