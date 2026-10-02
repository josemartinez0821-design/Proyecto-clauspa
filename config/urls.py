"""Direcciones del sitio de Claudia Spa."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

admin.site.index_title = "Inicio"

urlpatterns = [
    path("panel/", admin.site.urls),
]

if settings.DEBUG:
    # En desarrollo, Django sirve las fotos subidas. En el servidor lo hará el servidor web.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
