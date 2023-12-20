from django.db import transaction
from rest_framework import serializers

from networks.models import TradeLink, Product, Contact


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'product_launch_date']


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Contact
        fields = ['id', 'email', 'country', 'city', 'street', 'house_number']


class TradeLinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    products = ProductSerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)

    class Meta:
        model = TradeLink
        fields = ['id', 'name', 'supplier', 'debt', 'type', 'products', 'contacts']

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        contacts_data = validated_data.pop('contacts', [])
        tradelink = TradeLink.objects.create(**validated_data)

        self._handle_products(products_data, tradelink)
        self._handle_contacts(contacts_data, tradelink)

        return tradelink

    @transaction.atomic
    def update(self, instance, validated_data):

        products_data = validated_data.pop('products', [])
        contacts_data = validated_data.pop('contacts', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        self._handle_products(products_data, instance)
        self._handle_contacts(contacts_data, instance)

        return instance

    def _handle_products(self, products_data, tradelink_instance):

        for product_data in products_data:
            product_id = product_data.get('id')
            if product_id:
                product = Product.objects.get(id=product_id)
                for attr, value in product_data.items():
                    setattr(product, attr, value)
                product.save()
                product.suppliers.add(tradelink_instance)
            else:
                new_product = Product.objects.create(**product_data)
                new_product.suppliers.add(tradelink_instance)

    def _handle_contacts(self, contacts_data, tradelink_instance):
        for contact_data in contacts_data:
            contact_id = contact_data.get('id')
            if contact_id:
                contact = Contact.objects.get(id=contact_id)
                for attr, value in contact_data.items():
                    setattr(contact, attr, value)
                contact.save()
            else:
                Contact.objects.create(organization=tradelink_instance, **contact_data)