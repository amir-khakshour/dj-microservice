from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext, gettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.validators import MinValueValidator


@python_2_unicode_compatible
class Order(models.Model):
    order_no = models.BigIntegerField(verbose_name=_('Order number'), unique=True)
    # customer = models.ForeignKey('customer.Customer', verbose_name=_('Customer'), on_delete=models.SET_NULL, null=True, blank=True)
    customer_id = models.PositiveIntegerField(verbose_name=_('Customer'))
    # product = models.ForeignKey('product.Product', verbose_name=_('Product'), on_delete=models.SET_NULL, null=True, blank=True)
    product_id = models.PositiveIntegerField(verbose_name=_('Product'))
    quantity = models.PositiveIntegerField(verbose_name=_('Quantity'))
    price_net = models.DecimalField(_('Net price'), decimal_places=2, max_digits=20,
                                    validators=[MinValueValidator(Decimal('0.01'))])
    price_gross = models.DecimalField(_('Gross price'), decimal_places=2, max_digits=20,
                                      validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        unique_together = ('customer_id', 'product_id', 'quantity')
        ordering = ['quantity']

    def __str__(self):
        return ugettext('Order: %(order_no)s quantity: %(quantity)s') % {
            'order_no': self.order_no,
            'quantity': self.quantity,
        }
