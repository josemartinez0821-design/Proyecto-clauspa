"""Páginas generales: Inicio, Nosotros, Contacto y aviso de privacidad."""

from django.shortcuts import render

from servicios.models import Servicio

from .models import Diapositiva, Negocio, PreguntaFrecuente, Tecnologia


def inicio(request):
    return render(
        request,
        "sitio/inicio.html",
        {
            "diapositivas": Diapositiva.objects.vigentes().select_related("servicio")[: Diapositiva.MAXIMO_ACTIVAS],
            "destacados": Servicio.objects.filter(visible=True, destacado=True).prefetch_related("fotos"),
            "tecnologia": Tecnologia.objects.filter(visible=True),
        },
    )


def nosotros(request):
    return render(request, "sitio/nosotros.html", {"fotos": Negocio.cargar().fotos_local.all()})


def contacto(request):
    return render(request, "sitio/contacto.html", {"preguntas": PreguntaFrecuente.objects.filter(visible=True)})


def privacidad(request):
    return render(request, "sitio/privacidad.html")
