from decimal import Decimal
from rest_framework import serializers
from ..models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OnDemandPriceSerializer(CustomerSerializer):
    price_net = serializers.DecimalField(max_digits=12, min_value=Decimal('0.01'), required=True, decimal_places=2)
    quantity = serializers.IntegerField(max_value=10**12, min_value=1, required=True)  # TODO change max_value based on some static settings
    price_gross = serializers.DecimalField(max_digits=12, min_value=Decimal('0.01'), read_only=True, decimal_places=2)

    class Meta:
        model = Customer
        fields = ('price_net', 'type', 'vat_percentage', 'quantity', 'price_gross')
