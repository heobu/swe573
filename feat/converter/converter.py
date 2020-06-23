import time


class CookingConverter:

    density = {
        "water": 1.0,
        "sugar, granulated": 0.8,
        "sugar, powdered": 0.9
    }

    volume_units = {
        "ml": 1,
        "l": 1000,
        "cup": 240,
        "teaspoon": 5,
        "tablespoon": 15,
        #"fl oz": 30
    }
    # 1 oz = 28 g

    synonyms = {
        "sugar, caster": "sugar, granulated"
    }

    # do the checks with lowercase/uppercase to remove some of these aliases
    alias = {
        "milliliter": "ml",
        "liter": "l",
        "tsp": "teaspoon",
        "teaspoon": "teaspoon",
        "tbsp": "tablespoon",
        "tablespoon": "tablespoon",
        "Kcal": "kcal",
        "kCal": "kcal",
        "KCAL": "kcal",
        "j": "J",
        "KJ": "kJ",
        "Kj": "kJ",
        "kj": "kJ"
    }

    mass_units = {
        "mg": 0.001,
        "g": 1,
        "kg": 1000
    }

    energy_units = {
        "cal": 1000,
        "kcal": 1,
        "J": 1/4184,
        "kJ": 1/4.184
    }

    standard_units = ["ml", "g", "kcal"]

    # Return 0 if the item is not known or the unit is not known.
    def volume_to_mass(self, quantity, unit, item):
        # mass = density * volume

        density = self.find_density(item)
        volume = self.find_volume_ml(quantity, unit)

        mass = density * volume
        #mass = float(mass.__format__(".2f"))

        return mass

    # Return 0 if the item is not known or the unit is not known.
    def find_density(self, item):
        density = 0
        if item in self.density:
            density = self.density[item]
        elif item in self.synonyms:
            density = self.density[self.synonyms[item]]
        else:
            print("Density of item '", item, "' is unknown.")
            pass
        return density

    # Return 0 if the unit is not known.
    def find_volume_ml(self, quantity, unit):
        if unit not in self.volume_units:
            if unit in self.alias:
                return quantity * self.alias[unit]
            else:
                print("Unit '", unit, "' is unknown.")
                return 0
        else:
            return quantity * self.volume_units[unit]

    # Return 0 if the unit is not known.
    def find_mass_g(self, quantity, unit):
        if unit not in self.mass_units:
            if unit in self.alias:
                return quantity * self.alias[unit]
            else:
                print("Unit '", unit, "' is unknown.")
                return 0
        else:
            return quantity * self.mass_units[unit]

    # Return 0 if the unit is not known.
    def find_energy_kcal(self, quantity, unit):
        if unit not in self.energy_units:
            if unit in self.alias:
                return quantity * self.alias[unit]
            else:
                print("Unit '", unit, "' is unknown.")
                return 0
        else:
            return quantity * self.energy_units[unit]

    # Return 0 if the unit is not known.
    def to_standard(self, quantity, unit, type):
        types_measured_in_mass = ["Water", "Protein", "Carbohydrates", "Total lipid (fat)", "Minerals", "Vitamins and Other Components"]
        if type == "Energy":
            return self.find_energy_kcal(quantity, unit)
        elif type in types_measured_in_mass:
            return self.find_mass_g(quantity, unit)
        #elif type == "Water":
        #    return self.find_volume_ml(quantity, unit)
        else:
            print("Conversion for unit type '", type, "' is not implemented.")
            return 0

    # Return 0 if the unit is not known.
    # def to_standard(self, quantity, unit):
    #     if unit in self.standard_units:
    #         return quantity
    #     elif unit in self.alias:
    #         base_unit = self.alias[unit]
    #         if base_unit in self.standard_units:
    #             return quantity
    #         else:
    #             # convert, e.g. l to ml
    #             if base_unit is self.energy_units:
    #                 self.find_energy_kcal(quantity, unit)
    #             elif base_unit is self.mass_units:
    #                 self.find_mass_g(quantity, unit)
    #             elif base_unit is self.volume_units:
    #                 self.find_volume_ml(quantity, unit)
    #             else:
    #                 print("Conversion for unit type '", unit, "' is not implemented.")
    #                 return 0
    #     else:
    #         print("Unit '", unit, "' is unknown.")
    #         return 0

    # def to_standard(self, quantity, unit):
    #     if unit in self.standard_units or unit in self.alias:
    #         return quantity
    #     else:
    #         if unit.startswith("kilo"):
    #             sub_unit = unit[4:]
    #             if sub_unit in self.standard_units:
    #
    #             elif sub_unit in self.alias:
    #
    #             else:
    #         elif unit.startswith("k"):
    #             pass
    #         return 23.9

    # def find_density_alt(self, item):
    #     try:
    #         density = self.density[item]
    #     except KeyError:
    #         synonym = self.find_synonym(item)
    #         if synonym != "":
    #             density = self.density[synonym]
    #         else:
    #             density = 0
    #
    #     return density
    #
    # def find_synonym(self, item):
    #     try:
    #         synonym = self.synonyms[item]
    #     except KeyError:
    #         synonym = ""
    #
    #     return synonym
