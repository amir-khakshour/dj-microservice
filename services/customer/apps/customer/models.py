from collections import OrderedDict

from django.db import models
from django.utils.translation import ugettext, gettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinValueValidator, MaxValueValidator


@python_2_unicode_compatible
class Customer(models.Model):
    CUSTOMER_TYPE_ENDUSER = 'E'
    CUSTOMER_TYPE_RESELLER = 'R'
    CUSTOMER_TYPE_RESELLER_HIGH_VOLUME = 'H'
    CUSTOMER_TYPES = OrderedDict((
        (CUSTOMER_TYPE_ENDUSER, _("End User")),
        (CUSTOMER_TYPE_RESELLER, _("Reseller")),
        (CUSTOMER_TYPE_RESELLER_HIGH_VOLUME, _("Reseller High Volume")),
    ))

    CUSTOMER_STATUS_ACTIVE = 'A'
    CUSTOMER_STATUS_DELETED = 'D'
    CUSTOMER_STATUSES = OrderedDict((
        (CUSTOMER_STATUS_ACTIVE, _("Active")),
        (CUSTOMER_STATUS_DELETED, _("Deleted")),
    ))

    name = models.CharField(verbose_name=_('name'), max_length=255)
    type = models.CharField(
        verbose_name=_('customer type'), max_length=1,
        choices=list(CUSTOMER_TYPES.items())
    )
    vat_percentage = models.PositiveSmallIntegerField(
        verbose_name=_('customer type'),
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    status = models.CharField(
        verbose_name=_('customer status'), max_length=1,
        choices=list(CUSTOMER_STATUSES.items()), default=CUSTOMER_STATUS_ACTIVE
    )

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return ugettext('Customer: %(name)s Type: %(type)s Status: %(status)s') % {
            'name': self.name,
            'type': self.CUSTOMER_TYPES[self.type],
            'status': self.CUSTOMER_STATUSES[self.status],
        }
