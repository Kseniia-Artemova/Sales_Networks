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
    list_filter = ('contacts__city',)

    def supplier_link(self, obj):
        if obj.supplier:
            link = reverse("admin:networks_tradelink_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', link, obj.supplier.name)
        return "-"
    supplier_link.short_description = 'Supplier'

    def clear_debt(self, request, queryset):
        queryset.update(debt=0)
    clear_debt.short_description = "Clear debt of selected"


admin.site.register(Contact)
admin.site.register(Product)
