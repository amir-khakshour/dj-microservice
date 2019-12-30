import factory
from factory import Faker, fuzzy

from .models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('license_plate')
    price_net = fuzzy.FuzzyDecimal(0.0, 10 ** (Product._meta.get_field('price_net').max_digits - 2))
    status = fuzzy.FuzzyChoice(Product.PRODUCT_STATUSES.keys())
