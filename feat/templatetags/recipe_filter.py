from django import template
import json

register = template.Library()


@register.filter
def get_nutritional_value(recipe, key):
    return json.loads(recipe.nutritional_value).get(key)


@register.filter
def times(n):
    return range(n)
