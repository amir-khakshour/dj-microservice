from collections import OrderedDict

from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext, gettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from .utils import check_is_ascii


def validate_product_name(name):
    if not check_is_ascii(name) or ' ' in name:
        raise ValidationError(_('Product Name must include only ascii chars and no whitespace'))


@python_2_unicode_compatible
class Product(models.Model):
    PRODUCT_STATUS_ACTIVE = 'A'
    PRODUCT_STATUS_INACTIVE = 'I'
    PRODUCT_STATUSES = OrderedDict((
        (PRODUCT_STATUS_ACTIVE, _("Active")),
        (PRODUCT_STATUS_INACTIVE, _("Inactive")),
    ))

    name = models.CharField(verbose_name=_('name'), max_length=255, validators=[validate_product_name])
    price_net = models.DecimalField(_('Net price'), decimal_places=2, max_digits=12,
                                    validators=[MinValueValidator(Decimal('0.01'))])
    status = models.CharField(
        verbose_name=_('product status'), max_length=1,
        choices=list(PRODUCT_STATUSES.items()), default=PRODUCT_STATUS_INACTIVE
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return ugettext('Product: %(name)s Status: %(status)s') % {
            'name': self.name,
            'status': self.PRODUCT_STATUSES[self.status],
        }
