EVENT_HANDLERS = {}

def event_handler(event_type: str):
    """
    A decorator that registers a function as a handler for a specific event_type.
    """
    def decorator(func):
        EVENT_HANDLERS[event_type] = func
        return func

    return decorator