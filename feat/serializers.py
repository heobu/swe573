from django.contrib.auth.models import User
from rest_framework import serializers

from feat.models import ConsumerProfile, ProviderProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ConsumerProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ConsumerProfile
        fields = ('date_of_birth',)


class ProviderProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ('location',)
