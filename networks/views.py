from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from networks.filters import CountryFilter
from networks.models import TradeLink
from networks.permissions import IsActive
from networks.serializers import TradeLinkSerializer


class TradeLinkViewSet(ModelViewSet):
    serializer_class = TradeLinkSerializer
    queryset = TradeLink.objects.all()
    # permission_classes = [IsActive]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CountryFilter
