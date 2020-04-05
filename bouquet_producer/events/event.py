class Event:
    def __init__(self, event_type: str, payload=None):
        self._type = event_type
        self._payload = payload

    @property
    def type(self) -> str:
        return self._type

    @property
    def payload(self):
        return self._payload
