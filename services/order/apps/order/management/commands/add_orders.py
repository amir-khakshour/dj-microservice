import random
from django.core.management.base import BaseCommand
from customer.models import Customer
from product.models import Product
from order.models import Order
from order.factories import OrderFactory


class Command(BaseCommand):
    help = "create demo orders"

    def add_arguments(self, parser):
        parser.add_argument(
            '--total', '-t', dest='total', default=10000, type=int,
            help='Total number of orders to generate',
        )

    def handle(self, *args, **options):
        print("Generating {} number of order".format(options['total']))
        items = OrderFactory.build_batch(int(options['total']))

        counter = 10000
        product_range = range(Product.objects.first().pk, Product.objects.last().pk + 1)
        customer_range = range(Product.objects.first().pk, Product.objects.last().pk + 1)

        def _presave_order(o):
            nonlocal counter
            o.order_no = counter
            o.customer_id = random.choice(customer_range)
            o.product_id = random.choice(product_range)
            counter += 1
            return o

        Order.objects.bulk_create(_presave_order(p) for p in items)
