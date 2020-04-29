from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_consumer = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)


class ConsumerProfile(models.Model):
    date_of_birth = models.DateField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="consumer_profile")


class ProviderProfile(models.Model):
    location = models.TextField(max_length=20, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="provider_profile")


@receiver(post_save, sender=User)
def create_profile(instance, **kwargs):
    if instance.is_provider:
        ProviderProfile.objects.get_or_create(user=instance)
    elif instance.is_consumer:
        ConsumerProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def update_profile(instance, **kwargs):
    if instance.is_provider:
        instance.provider_profile.save()
    elif instance.is_consumer:
        instance.consumer_profile.save()
