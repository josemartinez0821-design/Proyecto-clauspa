"""Filtros y etiquetas de las plantillas del sitio. Uso: {% load spa %}."""

import json

from django import template
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe

from contenido.imagenes import ANCHOS, nombre_variante

from .. import formato

register = template.Library()

# Copias pequeñas que ya se comprobó que existen (no cambian: si la foto cambia, cambia el nombre).
_variantes_existentes = set()


@register.filter
def srcset(archivo, ancho_maximo):
    """
    {{ foto.imagen|srcset:1600 }} → "…-480.webp 480w, …-960.webp 960w, ….webp 1600w".
    Solo incluye las copias que existen, para que una foto antigua nunca salga rota.
    """
    if not archivo:
        return ""
    ancho_maximo = int(ancho_maximo)
    partes = []
    for ancho in ANCHOS:
        if ancho >= ancho_maximo:
            continue
        variante = nombre_variante(archivo.name, ancho)
        if variante in _variantes_existentes or archivo.storage.exists(variante):
            _variantes_existentes.add(variante)
            partes.append(f"{archivo.storage.url(variante)} {ancho}w")
    partes.append(f"{archivo.url} {ancho_maximo}w")
    return ", ".join(partes)


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


DIAS_SCHEMA = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}


@register.simple_tag(takes_context=True)
def datos_negocio(context):
    """Datos del negocio para Google (schema.org/DaySpa, en JSON-LD): nombre, dirección, teléfono y horario."""
    request, negocio = context["request"], context["negocio"]
    sitio = f"{request.scheme}://{request.get_host()}"
    datos = {
        "@context": "https://schema.org",
        "@type": "DaySpa",
        "name": negocio.nombre,
        "slogan": negocio.lema,
        "url": sitio + reverse("inicio"),
        "image": sitio + static("img/logo-circulo.png"),
        "priceRange": "$$",
    }
    telefono = negocio.telefono or negocio.whatsapp
    if telefono:
        datos["telephone"] = f"+57{telefono}"
    if negocio.direccion:
        calle = f"{negocio.direccion}, Barrio {negocio.barrio}" if negocio.barrio else negocio.direccion
        datos["address"] = {"@type": "PostalAddress", "streetAddress": calle, "addressCountry": "CO"}
        if negocio.ciudad:
            datos["address"]["addressLocality"] = negocio.ciudad
    if negocio.enlace_mapa:
        datos["hasMap"] = negocio.enlace_mapa
    redes = [red for red in (negocio.instagram, negocio.facebook, negocio.tiktok) if red]
    if redes:
        datos["sameAs"] = redes
    datos["openingHoursSpecification"] = [
        {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": f"https://schema.org/{DIAS_SCHEMA[franja.dia_semana]}",
            "opens": f"{franja.hora_apertura:%H:%M}",
            "closes": f"{franja.hora_cierre:%H:%M}",
        }
        for franja in negocio.horarios.all()
    ]
    # Se escapan <, > y & para que ningún texto del panel pueda cerrar la etiqueta <script>.
    texto = json.dumps(datos, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return mark_safe(f'<script type="application/ld+json">{texto}</script>')


@register.simple_tag(takes_context=True)
def cita_whatsapp(context, servicio):
    """Enlace de WhatsApp con el mensaje para pedir cita de ese servicio (requisito S-09)."""
    negocio = context["negocio"]
    return negocio.enlace_whatsapp(
        f"Hola, vi la página de {negocio.nombre} y quiero pedir una cita para {servicio.nombre}."
    )
