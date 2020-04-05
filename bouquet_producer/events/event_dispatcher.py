from bouquet_producer.events.event import Event


class EventDispatcher:
    def __init__(self):
        self._events = dict()
        self.event_log = list()

    def has_listener(self, event_type: Event, listener) -> bool:
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        return False

    def dispatch_event(self, event: Event):
        if event.type in self._events.keys():
            listeners = self._events[event.type]

            for listener in listeners:
                listener(event)
        self.event_log.append(event)

    def add_event_listener(self, event_type: Event, listener) -> None:
        if not self.has_listener(event_type, listener):
            listeners = self._events.get(event_type, [])
            listeners.append(listener)
            self._events[event_type] = listeners

    def remove_event_listener(self, event_type: Event, listener) -> None:
        if self.has_listener(event_type, listener):
            listeners = self._events[event_type]
            if len(listeners) == 1:
                del self._events[event_type]
            else:
                listeners.remove(listener)
                self._events[event_type] = listeners
