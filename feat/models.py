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
            #ProviderProfile.objects.get_or_create(user=instance)
            provider_profile = ProviderProfile(user=instance)
            provider_profile.save()
        elif instance.is_consumer:
            #ConsumerProfile.objects.get_or_create(user=instance)
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
    ingredients = models.TextField(max_length=100, null=False)
    description = models.TextField(max_length=300, null=False)
    # picture (optional)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="recipe_creator")
    created_at = models.DateTimeField(auto_now_add=True)
    difficulty = models.IntegerField(null=False)
    prepared_in = models.IntegerField(null=False)