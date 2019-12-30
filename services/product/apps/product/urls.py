from django.conf.urls import url, include
from rest_framework import routers
from django.conf import settings
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .api.views import (
    ProductViewSet,
)

schema_view = get_schema_view(title='Product API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

router = routers.DefaultRouter()

router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    url(r'^%s/' % settings.API_BASE_PATH, include(router.urls)),
    url(r'^%s/docs' % settings.API_BASE_PATH, schema_view),
]
