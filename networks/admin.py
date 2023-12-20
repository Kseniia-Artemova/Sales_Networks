from django.contrib import admin
from django.utils.html import format_html
from rest_framework.reverse import reverse

from networks.models import TradeLink, Contact, Product


@admin.register(TradeLink)
class TradeLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'supplier_link', 'debt', 'type', 'created_at')
    actions = ['clear_debt']
    model = TradeLink
    fields = ('name', 'supplier', 'debt', 'type')

    def supplier_link(self, obj):
        if obj.supplier:
            link = reverse("admin:networks_tradelink_change", args=[obj.supplier.id])  # appname замените на имя вашего приложения
            return format_html('<a href="{}">{}</a>', link, obj.supplier.name)
        return "-"
    supplier_link.short_description = 'Supplier'

    def clear_debt(self, request, queryset):
        queryset.update(debt=0)
    clear_debt.short_description = "Clear debt of selected"

    class CityFilter(admin.SimpleListFilter):
        title = 'city'
        parameter_name = 'city'

        def lookups(self, request, model_admin):
            cities = Contact.objects.order_by('city').distinct('city').values_list('city', flat=True)
            return [(city, city) for city in cities]

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(contacts__city=self.value()).distinct()
            return queryset

    list_filter = (CityFilter,)


admin.site.register(Contact)
admin.site.register(Product)
