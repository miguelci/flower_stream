import unittest
from unittest.mock import patch

from bouquet_producer.events.available_events import AvailableEvents
from bouquet_producer.events.event import Event
from bouquet_producer.objects.flower import Flower
from bouquet_producer.entities.warehouse import Warehouse


@patch('bouquet_producer.events.event_dispatcher.EventDispatcher')
class WarehouseTest(unittest.TestCase):

    def test_adding_flowers(self, dispatcher):
        flower = Flower('a', 1)

        warehouse = Warehouse(dispatcher)
        warehouse.add_flower(flower)

        self.assertEqual({'a': 1}, warehouse.get_stock())
        dispatcher.dispatch_event.assert_called_once()

    def test_removing_flowers_by_event(self, dispatcher):
        warehouse = Warehouse(dispatcher)
        warehouse.add_flower(Flower('a', 1))
        warehouse.add_flower(Flower('b', 1))

        self.assertEqual({'a': 1, 'b': 1}, warehouse.get_stock())
        warehouse.remove_flowers(Event(AvailableEvents.FLOWER_REMOVED, Flower('a', 1)))
        self.assertEqual({'a': 0, 'b': 1}, warehouse.get_stock())

        dispatcher.dispatch_event.assert_called()

    def test_removing_flowers_that_do_not_exist_doesnt_return_error(self, dispatcher):
        warehouse = Warehouse(dispatcher)
        warehouse.add_flower(Flower('a', 1))
        warehouse.add_flower(Flower('b', 1))

        self.assertEqual({'a': 1, 'b': 1}, warehouse.get_stock())
        warehouse.remove_flowers(Event(AvailableEvents.FLOWER_REMOVED, Flower('c', 1)))
        self.assertEqual({'a': 1, 'b': 1}, warehouse.get_stock())

        dispatcher.dispatch_event.assert_called()


if __name__ == '__main__':
    unittest.main()
