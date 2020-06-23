import ast

from django import template
import json
import re

register = template.Library()


@register.filter
def get_nutritional_value(recipe, key):
    return json.loads(recipe.nutritional_value).get(key)

#{'Energy': 567.64, 'Protein': 65.878, 'Carbohydrates': 0.0, 'Total lipid (fat)': 2.7927999999999997, 'Minerals': 0.0, 'Vitamins and Other Components': 0.0, 'Water': 702.66}
@register.filter
def filter_nutritional_value(nutritional_value, key):
    return ast.literal_eval(nutritional_value)[key]


@register.filter
def split_ingredients(ingredients):
    pattern = r'([\w*(,\s)?]+)\(([0-9]*)\)\:([\w*(,\s)?]+)\:([0-9]*)\;'
    r = re.compile(pattern)
    ingredients_list = r.findall(ingredients)
    return ingredients_list


#('Bananas, overripe, raw', '790774', 'Banana', '2')
@register.filter
def second(ingredient):
    return ingredient[1]

@register.filter
def third(ingredient):
    return ingredient[2]

@register.filter
def fourth(ingredient):
    return ingredient[3]

#{'Energy': 567.64, 'Protein': 65.878, 'Carbohydrates': 0.0, 'Total lipid (fat)': 2.7927999999999997, 'Minerals': 0.0, 'Vitamins and Other Components': 0.0, 'Water': 702.66}
##@register.filter
##def get_nutritional_value(nutritional_value, key):
##    return json.loads(nutritional_value).get(key)

@register.filter
def times(n):
    return range(n)


# recipe.recipelike.cprofiles.all|cprofilecontains:user.consumer_profile
@register.filter
def cprofiles_contains(cprofiles, profile):
    print(cprofiles)
    print(profile)
    return profile in cprofiles