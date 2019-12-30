from django_filters import rest_framework as filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from ..models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter


class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilter

