from django.db import models


class TradeLink(models.Model):
    """
    Модель звена торговой цепи
    """

    TYPE_CHOICES = [
        (0, 'Factory'),
        (1, 'Retail'),
        (2, 'Entrepreneur')
    ]

    name = models.CharField(max_length=255, verbose_name="Name")
    supplier = models.ForeignKey('TradeLink',
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name="Supplier")
    debt = models.DecimalField(blank=True, null=True, default=0, max_digits=10, decimal_places=2, verbose_name="Debt")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name="Type")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель товара
    """

    name = models.CharField(max_length=255, verbose_name="Name")
    model = models.CharField(max_length=255, verbose_name="Model")
    product_launch_date = models.DateTimeField(verbose_name="Product Launch Date")
    suppliers = models.ManyToManyField(TradeLink, related_name='products', verbose_name="Suppliers")

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Модель контактных данных
    """

    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=255, verbose_name="Country")
    city = models.CharField(max_length=255, verbose_name="City")
    street = models.CharField(max_length=255, verbose_name="Street")
    house_number = models.CharField(max_length=20, verbose_name="House Number")
    organization = models.ForeignKey(TradeLink,
                                     on_delete=models.CASCADE,
                                     related_name='contacts',
                                     verbose_name="Organization")

    def __str__(self):
        return self.email