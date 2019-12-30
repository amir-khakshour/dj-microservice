from decimal import Decimal, ROUND_DOWN

from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters import rest_framework as filters

from ..models import Customer
from .serializers import CustomerSerializer, OnDemandPriceSerializer
from .filters import CustomerFilter


class CustomerViewSet(ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = CustomerFilter

    @action(detail=False, url_path='get_price', methods=['get'])
    def get_price(self, request, *args, **kwargs):
        # gridscale: GET /api/1.0/customer/get_price/?price_net=12&type=R&vat_percentage=8&quantity=51
        # Since there is two fields from query_params in our customer model we can
        # validate those fields using customer serializer and also define an action method instead of a independent PriceApi endpoint
        # for simplicity of usage we use query params instead of data (POST data)
        serializer = OnDemandPriceSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # TODO: follow open-close principle
        # calculate rebate
        rebate_table = {
            Customer.CUSTOMER_TYPE_ENDUSER: 0,
            Customer.CUSTOMER_TYPE_RESELLER: 5,
            Customer.CUSTOMER_TYPE_RESELLER_HIGH_VOLUME: 7,
        }
        rebate = rebate_table[serializer.data['type']]
        if serializer.data['quantity'] >= 10:
            rebate += 2 if serializer.data['quantity'] >= 50 else 1
        return_data = serializer.data
        price_gross = ((Decimal(rebate) / Decimal(100)) + Decimal(1)) * \
                                     Decimal(serializer.data['price_net']) * \
                                     (Decimal(serializer.data['vat_percentage']) / Decimal(100) + 1) * serializer.data['quantity']

        return_data['price_gross'] = Decimal(price_gross).quantize(Decimal('.01'), rounding=ROUND_DOWN)
        return_data['price_net'] = Decimal(Decimal(return_data['price_net']) * serializer.data['quantity'])\
            .quantize(Decimal('.01'), rounding=ROUND_DOWN)
        return Response(return_data, status=status.HTTP_200_OK)
