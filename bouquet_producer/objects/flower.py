class Flower:

    NO_FLOWER = 'No flower'

    def __init__(self, specie: str, amount: int):
        self._specie = specie
        self._amount = amount

    @property
    def specie(self) -> str:
        return self._specie

    @property
    def amount(self) -> int:
        return self._amount

    def __str__(self):
        return '{},{}'.format(self.specie, self.amount)
