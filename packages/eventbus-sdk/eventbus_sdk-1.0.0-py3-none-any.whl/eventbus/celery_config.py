import os
from celery import Celery
from kombu import Queue, Exchange
from dotenv import load_dotenv
from routes import ROUTES

load_dotenv()

SERVICE_NAME = os.environ["SERVICE_NAME"]

RABBIT_HOST = os.environ["AWS_MQ_RABBITMQ_URL"]
RABBIT_PORT = os.getenv("AWS_MQ_RABBITMQ_PORT", "5671")
RABBIT_USER = os.getenv("AWS_MQ_RABBITMQ_USER", "guest")
RABBIT_PASS = os.getenv("AWS_MQ_RABBITMQ_PASSWORD", "guest")

BROKER_URL = f'amqps://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}'

app = Celery('eventbus')
app.conf.update({
    'broker_url': BROKER_URL,
    'task_routes': ROUTES,
    'task_queues': (
        Queue('broadcast_events', Exchange('broadcast_events', type='fanout', durable=True),
              routing_key='broadcast_events'),
    ),
})
