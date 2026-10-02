"""Páginas generales: Inicio, Nosotros, Contacto, aviso de privacidad y robots.txt."""

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from servicios.models import Servicio

from .models import Diapositiva, Negocio, PreguntaFrecuente, Tecnologia


def inicio(request):
    diapositivas = list(Diapositiva.objects.vigentes().select_related("servicio")[: Diapositiva.MAXIMO_ACTIVAS])
    return render(
        request,
        "sitio/inicio.html",
        {
            "diapositivas": diapositivas,
            "destacados": Servicio.objects.filter(visible=True, destacado=True).prefetch_related("fotos"),
            "tecnologia": Tecnologia.objects.filter(visible=True),
            "seo_imagen": diapositivas[0].imagen.url if diapositivas else "",
        },
    )


def nosotros(request):
    return render(
        request,
        "sitio/nosotros.html",
        {
            "fotos": Negocio.cargar().fotos_local.all(),
            "seo_titulo": "Nosotros",
            "seo_descripcion": "Atención personalizada en tratamientos faciales y corporales. Conoce nuestra historia.",
        },
    )


def contacto(request):
    return render(
        request,
        "sitio/contacto.html",
        {
            "preguntas": PreguntaFrecuente.objects.filter(visible=True),
            "seo_titulo": "Contacto",
            "seo_descripcion": "Dirección, horario, WhatsApp y teléfono. Escríbenos y pide tu cita.",
        },
    )


def privacidad(request):
    return render(
        request,
        "sitio/privacidad.html",
        {"seo_titulo": "Aviso de privacidad", "seo_descripcion": "Qué datos personales usamos y para qué."},
    )


@require_GET
def robots(request):
    """Le dice a Google qué puede revisar: todo menos el panel, y dónde está el mapa del sitio."""
    sitemap = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    lineas = ["User-agent: *", f"Disallow: {reverse('admin:index')}", f"Sitemap: {sitemap}"]
    return HttpResponse("\n".join(lineas) + "\n", content_type="text/plain; charset=utf-8")
