import time


class CookingConverter:

    density = {
        "water": 1.0,
        "sugar, granulated": 0.8,
        "sugar, powdered": 0.9
    }

    units = {
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

    alias = {
        "milliliter": "ml",
        "liter": "l",
        "tsp": "teaspoon",
        "teaspoon": "teaspoon",
        "tbsp": "tablespoon",
        "tablespoon": "tablespoon",
    }

    # Return 0 if the item is not known or the unit is not known.
    def volume_to_mass(self, quantity, unit, item):
        # mass = density * volume

        density = self.find_density(item)
        volume = self.find_volume_ml(quantity, unit)

        mass = density * volume
        #mass = float(mass.__format__(".2f"))

        return mass

    def find_density(self, item):
        density = 0
        if item in self.density:
            density = self.density[item]
        elif item in self.synonyms:
            density = self.density[self.synonyms[item]]
        else:
            pass
        return density

    # Return 0 if the unit is not known.
    def find_volume_ml(self, quantity, unit):
        if unit not in self.units:
            if unit in self.alias:
                return quantity * self.alias[unit]
            else:
                return 0
        else:
            return quantity * self.units[unit]

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
