from bouquet_producer.events.available_events import AvailableEvents
from bouquet_producer.objects.bouquet import Bouquet
from bouquet_producer.events.event import Event
from bouquet_producer.events.event_dispatcher import EventDispatcher


class Output:
    def __init__(self, event_dispatcher: EventDispatcher):
        event_dispatcher.add_event_listener(AvailableEvents.BOUQUET_DESIGN_COMPLETED,
                                            self.output_bouquet)

    @staticmethod
    def output_bouquet(event: Event) -> None:
        bouquet = event.payload

        if isinstance(bouquet, Bouquet):
            print(bouquet)
