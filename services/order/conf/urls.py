from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(('order.urls', 'order'), namespace="order")),
]


# @TODO remove on production
urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

if settings.DEBUG:
    import debug_toolbar  # noqa

    urlpatterns = urlpatterns + [
        url('admin/__debug__/', include(debug_toolbar.urls)),
        # catch all rule so that we can navigate to
        # routes in vue app other than "/"
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
