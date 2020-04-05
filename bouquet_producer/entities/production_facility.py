from random import randint

from bouquet_producer.events.available_events import AvailableEvents
from bouquet_producer.objects.bouquet import Bouquet
from bouquet_producer.events.event import Event
from bouquet_producer.events.event_dispatcher import EventDispatcher
from bouquet_producer.objects.flower import Flower


class ProductionFacility:
    def __init__(self, event_dispatcher: EventDispatcher):
        self._bouquets = list()
        self._event_dispatcher = event_dispatcher

        event_dispatcher.add_event_listener(AvailableEvents.FLOWER_ADDED_TO_STOCK,
                                            self.check_warehouse_stock_for_bouquet)

    def bouquet(self):
        return self._bouquets

    def add_bouquet(self, str_bouquet: str):
        self._bouquets.append(Bouquet.parse_bouquet(str_bouquet))

    def check_warehouse_stock_for_bouquet(self, event: Event):
        flower_stock = event.payload.copy()
        for bouquet in self._bouquets:
            if bouquet.current_total < bouquet.flower_quantity:
                for flower_specie in bouquet.flowers:
                    self.get_species_from_stock_for_bouquet(bouquet, flower_specie, flower_stock)

            if bouquet.flower_quantity <= bouquet.current_total < bouquet.total_flowers:
                flower = self.take_random_flowers(
                    bouquet.size, bouquet.total_flowers - bouquet.flower_quantity, flower_stock)

                if flower.specie is not Flower.NO_FLOWER and flower.amount != 0:
                    bouquet.add_specie_amount(Flower(flower.specie, flower.amount))
                    self.update_flower_numbers(bouquet, flower_stock, flower.specie, flower.amount)
            self.is_bouquet_complete(bouquet)

        self.are_there_still_bouquets_to_fill()

    def get_species_from_stock_for_bouquet(self, bouquet, flower_specie, flower_stock):
        if flower_specie in flower_stock and flower_stock[flower_specie] > 0:
            amount_needed = bouquet.flowers_for_operations[flower_specie]
            current_stock_amount = flower_stock[flower_specie]
            flowers_to_remove = self.get_flowers_to_remove_from_stock(
                amount_needed, current_stock_amount
            )
            bouquet.flowers_for_operations[flower_specie] -= flowers_to_remove
            self.update_flower_numbers(bouquet, flower_stock, flower_specie, flowers_to_remove)

    def is_bouquet_complete(self, bouquet):
        if bouquet.current_total == bouquet.total_flowers:
            self._bouquets.remove(bouquet)
            self._event_dispatcher.dispatch_event(Event(AvailableEvents.BOUQUET_DESIGN_COMPLETED, bouquet))

    def are_there_still_bouquets_to_fill(self):
        if len(self._bouquets) == 0:
            self._event_dispatcher.dispatch_event(Event(AvailableEvents.NO_MORE_BOUQUETS))

    def update_flower_numbers(self, bouquet: Bouquet, flower_stock, flower_specie: str, flowers_to_remove: int) -> None:
        if flowers_to_remove == 0:
            return
        flower_stock[flower_specie] -= flowers_to_remove
        bouquet.current_total += flowers_to_remove
        self._event_dispatcher.dispatch_event(
            Event(AvailableEvents.FLOWER_REMOVED, Flower(flower_specie, flowers_to_remove)))

    @staticmethod
    def take_random_flowers(bouquet_size: chr, flowers_still_to_retrieve: int, flower_stock: dict) -> Flower:
        if bouquet_size == 'L':
            random_flowers = dict(filter(lambda elem: elem[0].isupper() and elem[1] > 0, flower_stock.items()))
        else:
            random_flowers = dict(filter(lambda elem: elem[0].islower() and elem[1] > 0, flower_stock.items()))

        if len(random_flowers) == 0:
            return Flower(Flower.NO_FLOWER, 0)

        specie = list(random_flowers)[randint(0, len(random_flowers) - 1)]

        flowers_to_remove = ProductionFacility.get_flowers_to_remove_from_stock(
            flowers_still_to_retrieve, flower_stock[specie]
        )

        return Flower(specie, flowers_to_remove)

    @staticmethod
    def get_flowers_to_remove_from_stock(amount_needed: int, specie_stock_amount: int) -> int:
        if specie_stock_amount > amount_needed:
            return amount_needed
        return specie_stock_amount
