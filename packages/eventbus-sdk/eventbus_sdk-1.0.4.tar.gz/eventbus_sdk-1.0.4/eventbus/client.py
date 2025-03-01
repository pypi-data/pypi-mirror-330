from eventbus.worker import app


class EventClient:
    """
    A client for sending events between services.
    """

    @staticmethod
    def send_broadcast(event_type: str, payload: dict):
        """
        Send a broadcast event to all services.
        """
        EventClient._validate_event(event_type, payload)

        app.send_task(
            "events.broadcast",
            kwargs={"event_type": event_type, "payload": payload}
        )

    @staticmethod
    def send_direct(service_name: str, event_type: str, payload: dict):
        """
        Send a direct event to a specific service.
        """
        if not service_name or not isinstance(service_name, str):
            raise ValueError("`service_name` must be a non-empty string")

        EventClient._validate_event(event_type, payload)

        app.send_task(
            f"events.{service_name}",
            kwargs={"event_type": event_type, "payload": payload},
            routing_key=service_name
        )

    @staticmethod
    def _validate_event(event_type: str, payload: dict):
        """
        Validates event type and payload.
        """
        if not event_type or not isinstance(event_type, str):
            raise ValueError("`event_type` must be a non-empty string")

        if not isinstance(payload, dict):
            raise TypeError("`payload` must be a dictionary")

        if not payload:
            raise ValueError("`payload` cannot be empty")