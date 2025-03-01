import os

from dotenv import load_dotenv

load_dotenv()


SERVICES_NAME = os.getenv("SERVICES_NAME", "").split(",")
SERVICES_NAME = [service.strip() for service in SERVICES_NAME if service.strip()]

def create_direct_routes(services):
    """ Generates direct routing for each service. """
    return {
        f'events.{service}.*': {
            'queue': f'{service}_queue',
            'exchange': 'services_exchange',
            'exchange_type': 'direct',
            'routing_key': service
        }
        for service in services
    }

BROADCAST_ROUTES = {
    'events.*': {
        'queue': 'broadcast_events',
        'exchange': 'broadcast_events',
        'exchange_type': 'fanout',
        'binding_key': 'broadcast_events'
    }
}

ROUTES = {**BROADCAST_ROUTES, **create_direct_routes(SERVICES_NAME)}
