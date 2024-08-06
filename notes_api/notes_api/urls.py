from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include, 
    path, 
)

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title=settings.SWAGGER_INFO['title'],
        default_version=settings.SWAGGER_INFO['version'],
        description=settings.SWAGGER_INFO['description'],
        terms_of_service=settings.SWAGGER_INFO['type_of_service'],
        contact=openapi.Contact(email=settings.SWAGGER_INFO['contact_email']),
        license=openapi.License(name=settings.SWAGGER_INFO['license_name']),
    ),
    public=settings.SWAGGER_INFO['is_public'],
    permission_classes=[permissions.AllowAny],
    url=settings.APP_URL,
)

urlpatterns = [
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('', include('api.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)