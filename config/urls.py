"""Direcciones del sitio de Claudia Spa."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from contenido import views as contenido
from contenido.sitemaps import SITEMAPS
from servicios import views as servicios
from servicios.models import Servicio

admin.site.index_title = "Inicio"

FACIAL, CORPORAL = Servicio.Categoria.FACIAL, Servicio.Categoria.CORPORAL

urlpatterns = [
    path("panel/", admin.site.urls),
    path("", contenido.inicio, name="inicio"),
    path("faciales/", servicios.categoria, {"categoria": FACIAL}, name="faciales"),
    path("faciales/<slug:slug>/", servicios.detalle, {"categoria": FACIAL}, name="detalle_facial"),
    path("corporales/", servicios.categoria, {"categoria": CORPORAL}, name="corporales"),
    path("corporales/<slug:slug>/", servicios.detalle, {"categoria": CORPORAL}, name="detalle_corporal"),
    path("nosotros/", contenido.nosotros, name="nosotros"),
    path("contacto/", contenido.contacto, name="contacto"),
    path("aviso-de-privacidad/", contenido.privacidad, name="privacidad"),
    # Para Google
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", contenido.robots, name="robots"),
]

if settings.DEBUG:
    # En desarrollo, Django sirve las fotos subidas. En el servidor lo hará el servidor web.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
