from django.core.management.base import BaseCommand
from customer.models import Customer
from customer.factories import CustomerFactory


class Command(BaseCommand):
    help = "create demo customers"

    def add_arguments(self, parser):
        parser.add_argument(
            '--total', '-t', dest='total', default=10000, type=int,
            help='Total number of customers to generate',
        )
        parser.add_argument(
            '--status', '-s', dest='status', default=Customer.CUSTOMER_STATUS_ACTIVE, type=str,
            help='Status of generated models',
        )

    def handle(self, *args, **options):
        print("Generating {} number of customers".format(options['total']))
        assert options['status'] in Customer.CUSTOMER_STATUSES.keys(), "Please enter a valid status from: %s" % Customer.CUSTOMER_STATUSES
        Customer.objects.bulk_create(CustomerFactory.build_batch(int(options['total']), status=options['status']))

