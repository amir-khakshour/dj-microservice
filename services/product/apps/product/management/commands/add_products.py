from django.core.management.base import BaseCommand
from product.models import Product
from product.factories import ProductFactory


class Command(BaseCommand):
    help = "create demo products"

    def add_arguments(self, parser):
        parser.add_argument(
            '--total', '-t', dest='total', default=10000, type=int,
            help='Total number of products to generate',
        )
        parser.add_argument(
            '--status', '-s', dest='status', default=Product.PRODUCT_STATUS_ACTIVE, type=str,
            help='Status of generated models',
        )

    def handle(self, *args, **options):
        print("Generating {} number of products".format(options['total']))
        assert options['status'] in Product.PRODUCT_STATUSES.keys(), "Please enter a valid status from: %s" % Product.PRODUCT_STATUS_ACTIVE
        products = ProductFactory.build_batch(int(options['total']), status=options['status'])

        def _fix_name(p):
            p.name = p.name.replace(' ', '')
            return p

        Product.objects.bulk_create((_fix_name(p) for p in products))
