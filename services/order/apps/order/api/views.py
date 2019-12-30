import csv
from django.http import StreamingHttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from rest_framework_csv.renderers import CSVRenderer

from ..models import Order
from .serializers import OrderSerializer, OrderCSVSerializer


class OrderApiViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    @action(detail=False, url_path='get_csv', methods=['get'], renderer_classes=[CSVRenderer, ])
    def get_csv(self, request, *args, **kwargs):
        """A view that streams a large CSV file."""
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer_class = OrderCSVSerializer
        kwargs['context'] = self.get_serializer_context()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)
