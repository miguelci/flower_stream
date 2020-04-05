import re

from bouquet_producer.objects.flower import Flower


class Bouquet:
    def __init__(self, name: chr, size: chr, total_flowers: int, flower_quantity: int, flowers: dict):
        self.name = name
        self.size = size
        self.total_flowers = total_flowers
        self.flowers = flowers
        self.flower_quantity = flower_quantity
        self.current_total = 0
        self.flowers_for_operations = flowers.copy()

    def add_specie_amount(self, flower: Flower):
        specie, amount = flower.specie, flower.amount
        if specie not in self.flowers:
            self.flowers[specie] = amount
        else:
            self.flowers[specie] += amount

    @staticmethod
    def parse_bouquet(bouquet: str):
        name, size = bouquet[0], bouquet[1]
        only_flowers = re.split(r'([a-z]+)', bouquet[2:])
        total_flowers = int(only_flowers[-1])

        species = only_flowers[1:-1:2]
        if size == 'L':
            species = list(map(lambda specie: specie.capitalize(), species))
        flowers = dict(zip(species, map(int, only_flowers[0:-1:2])))
        flower_quantity = sum(flowers.values())

        return Bouquet(name, size, total_flowers, flower_quantity, flowers)

    def __str__(self):
        flowers = "".join(str(amount) + specie.lower() for specie, amount in self.flowers.items())
        return "{}{}{}".format(self.name, self.size, flowers)
