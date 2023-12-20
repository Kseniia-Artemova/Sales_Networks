from django.db import transaction
from rest_framework import serializers

from networks.models import TradeLink, Product, Contact


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'model', 'product_launch_date']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['email', 'country', 'city', 'street', 'house_number']


class TradeLinkSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    contacts = ContactSerializer(many=True)

    class Meta:
        model = TradeLink
        fields = ['name', 'supplier', 'debt', 'type', 'products', 'contacts']

    @transaction.atomic
    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        contacts_data = validated_data.pop('contacts', [])
        instance = TradeLink.objects.create(**validated_data)

        new_products = []
        new_contacts = []

        for product_data in products_data:
            new_product = Product(**product_data)
            new_products.append(new_product)

        for contact_data in contacts_data:
            new_contact = Contact(organization=instance, **contact_data)
            new_contacts.append(new_contact)

        Product.objects.bulk_create(new_products)
        Contact.objects.bulk_create(new_contacts)
        instance.products.add(*new_products)

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        products_data = validated_data.pop('products', [])
        contacts_data = validated_data.pop('contacts', [])

        for attr, value in validated_data.items():
            if attr == 'debt':
                raise serializers.ValidationError('Debt can not be changed')
            setattr(instance, attr, value)
        instance.save()

        new_products = []
        new_contacts = []
        existing_products = []
        existing_contacts = []

        for product_data in products_data:
            product_id = product_data.get('id')
            if product_id:
                product = Product.objects.filter(id=product_id).first()
                if product:
                    for attr, value in product_data.items():
                        if attr != 'id':
                            setattr(product, attr, value)
                    existing_products.append(product)
            else:
                new_product = Product(**product_data)
                new_products.append(new_product)

        for contact_data in contacts_data:
            contact_id = contact_data.get('id')
            if contact_id:
                contact = Contact.objects.filter(id=contact_id).first()
                for attr, value in contact_data.items():
                    if attr != 'id':
                        setattr(contact, attr, value)
                existing_contacts.append(contact)
            else:
                new_contact = Contact(organization=instance, **contact_data)
                new_contacts.append(new_contact)

        instance.products.add(*new_products)
        Product.objects.bulk_update(existing_products)
        Contact.objects.bulk_update(existing_contacts)

        return instance