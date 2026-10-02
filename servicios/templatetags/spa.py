"""Filtros y etiquetas de las plantillas del sitio. Uso: {% load spa %}."""

from django import template

from .. import formato

register = template.Library()


@register.filter
def pesos(valor):
    """{{ 90000|pesos }} → $90.000"""
    return formato.pesos(valor) if valor is not None else ""


@register.filter
def lineas(texto):
    """Los campos "uno por línea" del panel, como lista y sin líneas vacías."""
    return [linea.strip() for linea in (texto or "").splitlines() if linea.strip()]


@register.filter
def primer_parrafo(texto):
    """El texto hasta la primera línea en blanco (el panel guarda los saltos de línea como \\r\\n)."""
    return (texto or "").replace("\r\n", "\n").strip().split("\n\n")[0].strip()


@register.simple_tag(takes_context=True)
def cita_whatsapp(context, servicio):
    """Enlace de WhatsApp con el mensaje para pedir cita de ese servicio (requisito S-09)."""
    negocio = context["negocio"]
    return negocio.enlace_whatsapp(
        f"Hola, vi la página de {negocio.nombre} y quiero pedir una cita para {servicio.nombre}."
    )
