"""Página de inicio del panel de la dueña y permisos del menú lateral."""

from django.urls import reverse

from contenido.models import Diapositiva, PreguntaFrecuente
from servicios.models import Servicio


def solo_administrador(request):
    return request.user.is_superuser


def inicio(request, context):
    """Datos de la página de inicio del panel (la usa templates/admin/index.html)."""
    activas = Diapositiva.objects.filter(activa=True).count()
    context["resumen"] = [
        {
            "titulo": "Servicios visibles",
            "valor": f"{Servicio.objects.filter(visible=True).count()} de {Servicio.objects.count()}",
            "enlace": reverse("admin:servicios_servicio_changelist"),
        },
        {
            "titulo": "Diapositivas activas",
            "valor": f"{activas} de {Diapositiva.MAXIMO_ACTIVAS}",
            "enlace": reverse("admin:contenido_diapositiva_changelist"),
        },
        {
            "titulo": "Preguntas frecuentes",
            "valor": PreguntaFrecuente.objects.filter(visible=True).count(),
            "enlace": reverse("admin:contenido_preguntafrecuente_changelist"),
        },
    ]
    context["accesos"] = [
        {
            "titulo": "Servicios y precios",
            "texto": "Agregar, editar u ocultar servicios",
            "icono": "spa",
            "enlace": reverse("admin:servicios_servicio_changelist"),
        },
        {
            "titulo": "Cambiar el slider",
            "texto": "Promociones y fechas especiales",
            "icono": "view_carousel",
            "enlace": reverse("admin:contenido_diapositiva_changelist"),
        },
        {
            "titulo": "Horario y contacto",
            "texto": "Dirección, WhatsApp y redes",
            "icono": "schedule",
            "enlace": reverse("admin:contenido_negocio_changelist"),
        },
    ]
    return context
