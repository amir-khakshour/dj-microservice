import factory
from factory import Faker, fuzzy

from order.models import Order
from customer.factories import CustomerFactory
from product.factories import ProductFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    order_no = fuzzy.FuzzyInteger(1, 1000)
    customer = factory.SubFactory(CustomerFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = fuzzy.FuzzyInteger(1, 1000)
