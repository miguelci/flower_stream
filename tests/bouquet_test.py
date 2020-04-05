import unittest

from bouquet_producer.objects.bouquet import Bouquet
from bouquet_producer.objects.flower import Flower

DEFAULT_BOUQUET_DESIGN = 'AL10a15b5c30'


class BouquetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.bouquet = Bouquet.parse_bouquet(DEFAULT_BOUQUET_DESIGN)

    def test_can_parse_a_bouquet_design(self):
        self.assertEqual('AL10a15b5c', str(self.bouquet))
        self.assertEqual('A', self.bouquet.name)
        self.assertEqual('L', self.bouquet.size)
        self.assertEqual(30, self.bouquet.total_flowers)

    def test_can_add_specie_amount(self):
        self.assertNotIn('5x', str(self.bouquet))
        self.bouquet.add_specie_amount(Flower('x', 5))
        self.assertIn('5x', str(self.bouquet))


if __name__ == '__main__':
    unittest.main()
