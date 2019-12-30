# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import Customer


class TestOnDemandGrossPriceCalculatorViewSetAction(APITestCase):
    def setUp(self):
        super().setUp()
        self.api_url = reverse('customer:customer-get-price')

    gross_price_calculator_params = [
        # (type, quantity, vat_percentage, price_net, net_price)
        # case #1: type: Enduser, quantity <10   => rebate = 0,  price_gross = price_net
        (Customer.CUSTOMER_TYPE_ENDUSER, 9, 0, 100, 100),
        # case #2: type: Reseller, quantity <10   => rebate = 5,  price_gross = price_net * 1.05
        (Customer.CUSTOMER_TYPE_RESELLER, 9, 0, 100, 100 * 1.05),
        # case #3: type: Enduser, quantity: 10   => rebate = 1, price_gross = price_net * 1.01
        (Customer.CUSTOMER_TYPE_ENDUSER, 10, 0, 100, 100 * 1.01),
        # case #4: type: Enduser, quantity: 50   => rebate = 2, price_gross = price_net * 1.02
        (Customer.CUSTOMER_TYPE_ENDUSER, 50, 0, 100, 100 * 1.02),
    ]

    def test_ordering(self):
        prams_fields = ['type', 'quantity', 'vat_percentage', 'price_net', 'rebate']
        for params in self.gross_price_calculator_params:
            data = dict(zip(prams_fields, params))
            with self.subTest(data=data):
                response = self.client.get(self.api_url, data)
                self.assertEqual(response.data['price_gross'], data['rebate'])
