import logging
from eventbus.worker import app
from eventbus.registry import EVENT_HANDLERS

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
