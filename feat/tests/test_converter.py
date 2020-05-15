import unittest

from feat.converter.converter import CookingConverter


class CookingConverterTest(unittest.TestCase):
    def setUp(self):
        self.converter = CookingConverter()

    def test_cooking_converter(self):
        self.assertIsNotNone(self.converter)

    def test_conversion_from_ml_volume_to_g_mass(self):
        quantity = 100
        unit = "ml"

        item = "sugar, granulated"
        actual_mass = self.converter.volume_to_mass(quantity, unit, item)

        expected_mass = 80
        self.assertAlmostEqual(expected_mass, actual_mass)

        item = "sugar, powdered"
        actual_mass = self.converter.volume_to_mass(quantity, unit, item)

        expected_mass = 90
        self.assertAlmostEqual(expected_mass, actual_mass)

    def test_conversion_from_ml_volume_to_g_mass_synonym(self):
        quantity = 100
        unit = "ml"
        item = "sugar, caster"

        actual_mass = self.converter.volume_to_mass(quantity, unit, item)

        expected_mass = 80

        self.assertAlmostEqual(expected_mass, actual_mass)

    def test_conversion_from_cup_volume_to_g_mass(self):
        quantity = 1
        unit = "cup"
        item = "sugar, granulated"  # granulated sugar
        actual_mass = self.converter.volume_to_mass(quantity, unit, item)

        expected_mass = 192

        self.assertAlmostEqual(expected_mass, actual_mass)

    def test_conversion_from_unknown_volume_to_g_mass(self):
        quantity = 1
        unit = "jar"
        item = "sugar, granulated"  # granulated sugar
        actual_mass = self.converter.volume_to_mass(quantity, unit, item)

        expected_mass = 0

        self.assertAlmostEqual(expected_mass, actual_mass)

    def test_conversion_from_ml_volume_to_g_mass_unknown_synonym(self):
        quantity = 100
        unit = "ml"
        item = "sugar"

        actual_mass = self.converter.volume_to_mass(quantity, unit, item)

        expected_mass = 0

        self.assertAlmostEqual(expected_mass, actual_mass)

    def test_to_standard_for_a_standard_unit_of_energy(self):
        quantity = 100
        unit = "kcal"
        type = "Energy"

        actual = self.converter.to_standard(quantity, unit, type)

        expected = 100

        self.assertAlmostEqual(expected, actual)

    def test_to_standard_for_a_nonstandard_unit_of_energy(self):
        quantity = 100
        type = "Energy"

        unit = "kJ"

        actual = self.converter.to_standard(quantity, unit, type)

        expected = 23.9
        self.assertAlmostEqual(expected, actual, places=2)

        unit = "cal"

        actual = self.converter.to_standard(quantity, unit, type)

        expected = 100000
        self.assertAlmostEqual(expected, actual)

    def test_to_standard_for_a_standard_unit_of_mass(self):
        quantity = 100
        unit = "g"
        type = "Carbohydrates"

        actual = self.converter.to_standard(quantity, unit, type)

        expected = 100

        self.assertAlmostEqual(expected, actual)

    def test_to_standard_for_a_nonstandard_unit_of_mass(self):
        quantity = 100
        type = "Carbohydrates"

        #unit = "pound"
        #actual = self.converter.to_standard(quantity, unit, type)
        #expected = 23.9
        #self.assertAlmostEqual(expected, actual)

        unit = "kg"

        actual = self.converter.to_standard(quantity, unit, type)

        expected = 100000
        self.assertAlmostEqual(expected, actual)

    def test_to_standard_for_a_standard_unit_of_volume(self):
        quantity = 100
        unit = "ml"
        type = "Water"

        actual = self.converter.to_standard(quantity, unit, type)

        expected = 100

        self.assertAlmostEqual(expected, actual)

    def test_to_standard_for_a_nonstandard_unit_of_volume(self):
        quantity = 100
        type = "Water"

        #unit = "cm3"
        #actual = self.converter.to_standard(quantity, unit, type)
        #expected = 23.9
        #self.assertAlmostEqual(expected, actual)

        unit = "l"

        actual = self.converter.to_standard(quantity, unit, type)

        expected = 100000
        self.assertAlmostEqual(expected, actual)

    # def test_conversion_from_ml_volume_to_g_mass_word_order(self):
    #     volume = 100
    #     unit = "ml"
    #
    #     item = "granulated sugar"
    #     actual_mass = self.converter.volume_to_mass(volume, unit, item)
    #
    #     expected_mass = 70
    #     self.assertAlmostEqual(expected_mass, actual_mass)
    #
    #     item = "powdered sugar"
    #     actual_mass = self.converter.volume_to_mass(volume, unit, item)
    #
    #     expected_mass = 56
    #     self.assertAlmostEqual(expected_mass, actual_mass)

    # def test_conversion_from_ml_volume_to_g_mass_synonym_word_order(self):
    #     volume = 100
    #     unit = "ml"
    #     item = "caster sugar"
    #
    #     actual_mass = self.converter.volume_to_mass(volume, unit, item)
    #
    #     expected_mass = 70
    #
    #     self.assertAlmostEqual(expected_mass, actual_mass)


if __name__ == '__main__':
    unittest.main()
