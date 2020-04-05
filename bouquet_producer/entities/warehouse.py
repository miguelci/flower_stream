from bouquet_producer.events.available_events import AvailableEvents
from bouquet_producer.events.event import Event
from bouquet_producer.events.event_dispatcher import EventDispatcher
from bouquet_producer.objects.flower import Flower


class Warehouse:
    def __init__(self, event_dispatcher: EventDispatcher):
        self._flowers = dict()
        self.needs_more_flowers = True
        self._event_dispatcher = event_dispatcher

        self._event_dispatcher.add_event_listener(AvailableEvents.FLOWER_REMOVED, self.remove_flowers)
        self._event_dispatcher.add_event_listener(AvailableEvents.NO_MORE_BOUQUETS, self.stop_adding_flowers)

    def add_flower(self, flower: Flower):
        specie, size = flower.specie, flower.amount

        if size == 'L':
            specie = specie.capitalize()

        if specie not in self._flowers:
            self._flowers[specie] = 1
        else:
            self._flowers[specie] += 1

        self._event_dispatcher.dispatch_event(Event(AvailableEvents.FLOWER_ADDED_TO_STOCK, self._flowers))

    def remove_flowers(self, event: Event):
        flower = event.payload
        if flower.specie not in self._flowers:
            return

        self._flowers[flower.specie] -= flower.amount
        self._event_dispatcher.dispatch_event(Event(AvailableEvents.FLOWER_REMOVED_FROM_STOCK, flower))

    def stop_adding_flowers(self, _):
        self.needs_more_flowers = False

    def get_stock(self):
        return self._flowers
