"""Direcciones del sitio de Claudia Spa."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

admin.site.index_title = "Inicio"


def provisional(titulo, texto=""):
    """Página en construcción (etapa 4). En la etapa 5 cada una tendrá su vista."""
    return TemplateView.as_view(
        template_name="sitio/en_construccion.html", extra_context={"titulo": titulo, "texto": texto}
    )


urlpatterns = [
    path("panel/", admin.site.urls),
    path("", provisional("Inicio", "Relajación y belleza"), name="inicio"),
    path("faciales/", provisional("Faciales", "Tratamientos para el cuidado de tu rostro."), name="faciales"),
    path("corporales/", provisional("Corporales", "Bienestar y cuidado para tu cuerpo."), name="corporales"),
    path("nosotros/", provisional("Nosotros", "Conoce a quien cuida de ti."), name="nosotros"),
    path("contacto/", provisional("Contacto", "Escríbenos, llámanos o visítanos."), name="contacto"),
    path("aviso-de-privacidad/", provisional("Aviso de privacidad"), name="privacidad"),
]

if settings.DEBUG:
    # En desarrollo, Django sirve las fotos subidas. En el servidor lo hará el servidor web.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
