from django.conf.urls import url, include
from django.conf import settings
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

from .api.views import (
    OrderApiViewSet,
)

# Create our schema's view w/ the get_schema_view() helper method. Pass in the proper Renderers for swagger
schema_view = get_schema_view(title='Order API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

router = routers.DefaultRouter()
router.register(r'order', OrderApiViewSet, basename='order')

urlpatterns = [
    url(r'^%s/' % settings.API_BASE_PATH, include(router.urls)),
    url(r'^%s/docs' % settings.API_BASE_PATH, schema_view),
]

