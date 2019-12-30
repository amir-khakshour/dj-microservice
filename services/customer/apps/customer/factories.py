import factory
from factory import Faker, fuzzy

from .models import Customer


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = Faker('name')
    type = fuzzy.FuzzyChoice(Customer.CUSTOMER_TYPES.keys())
    vat_percentage = fuzzy.FuzzyInteger(0, 20)
    status = fuzzy.FuzzyChoice(Customer.CUSTOMER_STATUSES.keys())
