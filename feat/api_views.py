from rest_framework import viewsets

from feat.models import ConsumerProfile, ProviderProfile
from feat.serializers import ConsumerProfileSerializer, ProviderProfileSerializer


class ConsumerProfileViewSet(viewsets.ModelViewSet):
    queryset = ConsumerProfile.objects.all()
    serializer_class = ConsumerProfileSerializer

class ProviderProfileViewSet(viewsets.ModelViewSet):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer