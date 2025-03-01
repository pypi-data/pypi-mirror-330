import logging
import os

from celery import Celery
from dotenv import load_dotenv
from kombu import Queue, Exchange

from eventbus.registry import EVENT_HANDLERS
from eventbus.routes import ROUTES

load_dotenv()

SERVICE_NAME = os.environ["SERVICE_NAME"]

RABBIT_HOST = os.environ["AWS_MQ_RABBITMQ_URL"]
RABBIT_PORT = os.getenv("AWS_MQ_RABBITMQ_PORT", "5671")
RABBIT_USER = os.getenv("AWS_MQ_RABBITMQ_USER", "guest")
RABBIT_PASS = os.getenv("AWS_MQ_RABBITMQ_PASSWORD", "guest")

BROKER_URL = f'amqps://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}'

app = Celery('eventbus', include=['eventbus.handlers'])
app.conf.update({
    'broker_url': BROKER_URL,
    'task_routes': ROUTES,
    'task_queues': (
        Queue('broadcast_events', Exchange('broadcast_events', type='fanout', durable=True),
              routing_key='broadcast_events'),
    ),
})


@app.task(name="events.broadcast", broadcast=True)
def broadcast_event(event_type: str, payload: dict):
    """ Обробка broadcast-подій. """
    handler = EVENT_HANDLERS.get(event_type)

    if not handler:
        logging.info(f"[EVENTBUS] No handler for event_type = '{event_type}'")
        return

    logging.info(f"[EVENTBUS] Got event_type='{event_type}' | data={payload}")
    handler(**payload)


@app.task(name=f"events.{app.conf.get('SERVICE_NAME')}")
def direct_event(event_type: str, payload: dict):
    """ Обробка direct-подій. """
    handler = EVENT_HANDLERS.get(event_type)

    if not handler:
        logging.info(f"[EVENTBUS-DIRECT] No handler for event_type = '{event_type}'")
        return

    logging.info(f"[EVENTBUS-DIRECT] Got event_type='{event_type}' | data={payload}")
    handler(**payload)
