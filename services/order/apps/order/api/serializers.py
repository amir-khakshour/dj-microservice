from rest_framework import serializers

from ..models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderCSVSerializer(serializers.ModelSerializer):
    customer_id = serializers.IntegerField()
    product_name = serializers.CharField(source='product.name')

    class Meta:
        model = Order
        fields = ('order_no', 'customer_id', 'product_name', 'quantity')
