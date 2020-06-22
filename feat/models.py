import json

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_consumer = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)


class ConsumerProfile(models.Model):
    date_of_birth = models.DateField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="consumer_profile")


class ProviderProfile(models.Model):
    location = models.TextField(max_length=20, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="provider_profile")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print('****', created)
    if created:
        if instance.is_provider:
            # ProviderProfile.objects.get_or_create(user=instance)
            provider_profile = ProviderProfile(user=instance)
            provider_profile.save()
        elif instance.is_consumer:
            # ConsumerProfile.objects.get_or_create(user=instance)
            consumer_profile = ConsumerProfile(user=instance)
            consumer_profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print('----')
    if instance.is_provider:
        ProviderProfile.objects.get_or_create(user=instance)
    elif instance.is_consumer:
        ConsumerProfile.objects.get_or_create(user=instance)


class Recipe(models.Model):
    print('rrrr')
    title = models.TextField(max_length=40, null=False)
    ingredients = models.TextField(max_length=10000, null=False)
    nutritional_value = models.TextField(max_length=1000, null=False)
    description = models.TextField(max_length=3000, null=False)
    instructions = models.TextField(max_length=3000, null=False)
    # picture (optional)
    image_link = models.URLField(max_length=300, null=False, blank=False, default="https://raw.githubusercontent.com/heobu/swe573/feature/posts-like-dislike-follow/feat/static/assets/images/eco-slider-img-1.jpg")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="recipe_creator")
    created_at = models.DateTimeField(auto_now_add=True)
    difficulty = models.IntegerField(null=False)
    prepared_in = models.IntegerField(null=False)

    def get_like_count(self):
        return self.recipelike.cprofiles.count()


@receiver(post_save, sender=Recipe)
def create_recipe_like(sender, instance, created, **kwargs):
    print('rl****', created)
    if created:
        recipe_like = RecipeLike(recipe=instance)
        recipe_like.save()


@receiver(post_save, sender=Recipe)
def save_recipe_like(sender, instance, **kwargs):
    print('rl----')
    RecipeLike.objects.get_or_create(recipe=instance)


class FoodItem(models.Model):
    print('fififi')


class Menu(models.Model):
    print('mmmm')
    title = models.TextField(max_length=40, null=False)
    description = models.TextField(max_length=300, null=False)
    food_items = models.CharField(max_length=300)
    nutritional_value = models.TextField(max_length=1000, null=False)
    image_link = models.URLField(max_length=300, null=False, blank=False, default="https://raw.githubusercontent.com/heobu/swe573/feature/posts-like-dislike-follow/feat/static/assets/images/eco-slider-img-1.jpg")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="menu_creator")
    created_at = models.DateTimeField(auto_now_add=True)

    def set_food_items(self, food_items):
        self.food_items = json.dumps(food_items)

    def get_food_items(self):
        return json.loads(self.food_items)

    def get_like_count(self):
        return self.menulike.cprofiles.count()


@receiver(post_save, sender=Menu)
def create_menu_like(sender, instance, created, **kwargs):
    print('ml****', created)
    if created:
        menu_like = MenuLike(menu=instance)
        menu_like.save()


@receiver(post_save, sender=Menu)
def save_menu_like(sender, instance, **kwargs):
    print('ml----')
    MenuLike.objects.get_or_create(menu=instance)


class RecipeLike(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, null=False)
    cprofiles = models.ManyToManyField(ConsumerProfile)


class MenuLike(models.Model):
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE, null=False)
    cprofiles = models.ManyToManyField(ConsumerProfile)

class Comment(models.Model):
    content = models.TextField(max_length=300, null=False)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=False, related_name="comment")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="author")
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False, null=False)
