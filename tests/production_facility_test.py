import unittest
from unittest.mock import patch

from bouquet_producer.events.available_events import AvailableEvents
from bouquet_producer.events.event import Event
from bouquet_producer.objects.flower import Flower
from bouquet_producer.entities.production_facility import ProductionFacility


class MyTestCase(unittest.TestCase):

    @patch('bouquet_producer.objects.bouquet.Bouquet')
    @patch('bouquet_producer.events.event_dispatcher.EventDispatcher')
    def test_call_update_flowers_without_flowers_to_remove(self, dispatcher, bouquet):
        production_facility = ProductionFacility(dispatcher)
        production_facility.update_flower_numbers(bouquet, {}, 'a', 0)
        dispatcher.assert_not_called()

    @patch('bouquet_producer.events.event_dispatcher.EventDispatcher')
    def test_bouquet_list_is_cleared_after_bouquet_complete(self, dispatcher):
        production_facility = ProductionFacility(dispatcher)
        production_facility.add_bouquet('AL10a15b5c30')

        flowers_added_to_stock = Event(AvailableEvents.FLOWER_ADDED_TO_STOCK, {'A': 10, 'B': 15, 'C': 5})
        production_facility.check_warehouse_stock_for_bouquet(flowers_added_to_stock)

        self.assertEqual([], production_facility.bouquet())

        dispatcher.dispatch_event.assert_called()

    def test_random_returns_empty_when_size_is_not_available(self):
        flower = ProductionFacility.take_random_flowers('L', 2, {'a': 2, 'b': 2, 'c': 2})
        self.assertEqual(Flower.NO_FLOWER, flower.specie)
        self.assertEqual(0, flower.amount)

    def test_random_returns_flower_when_size_is_available(self):
        flower = ProductionFacility.take_random_flowers('L', 2, {'A': 2, 'b': 2, 'c': 2})
        self.assertEqual('A', flower.specie)
        self.assertEqual(2, flower.amount)

    def test_gets_correct_flowers_to_remove(self) -> None:
        self.assertEqual(2, ProductionFacility.get_flowers_to_remove_from_stock(3, 2))
        self.assertEqual(0, ProductionFacility.get_flowers_to_remove_from_stock(3, 0))
        self.assertEqual(3, ProductionFacility.get_flowers_to_remove_from_stock(3, 4))
        self.assertEqual(4, ProductionFacility.get_flowers_to_remove_from_stock(4, 4))


if __name__ == '__main__':
    unittest.main()
