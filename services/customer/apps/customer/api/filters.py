# django-rest-framework-filters
from django_filters import rest_framework as filters

from ..models import Customer


class CustomerFilter(filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            'id': ['exact'],
            'name': ['exact', 'in', 'startswith'],
            'status': ['exact'],
        }
