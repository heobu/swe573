from django import template
import json

register = template.Library()


@register.filter
def get_nutritional_value(recipe, key):
    return json.loads(recipe.nutritional_value).get(key)


@register.filter
def times(n):
    return range(n)


# recipe.recipelike.cprofiles.all|cprofilecontains:user.consumer_profile
@register.filter
def cprofiles_contains(cprofiles, profile):
    print(cprofiles)
    print(profile)
    return profile in cprofiles