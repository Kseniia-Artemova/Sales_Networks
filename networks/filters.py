import django_filters
from .models import TradeLink, Contact


class CountryFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(field_name='contacts__country', distinct=True)

    class Meta:
        model = TradeLink
        fields = ['country']