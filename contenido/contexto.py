"""Lo que usan todas las páginas del sitio: los datos del negocio (encabezado, pie, WhatsApp) y el menú."""

from django.urls import reverse
from django.utils.functional import SimpleLazyObject

from .models import Negocio

MENU = [
    ("Inicio", "inicio"),
    ("Faciales", "faciales"),
    ("Corporales", "corporales"),
    ("Nosotros", "nosotros"),
    ("Contacto", "contacto"),
]


def sitio(request):
    menu = []
    for titulo, nombre in MENU:
        url = reverse(nombre)
        # Inicio solo se marca en "/"; las demás también en sus subpáginas (/faciales/limpieza…/).
        activo = request.path == url if url == "/" else request.path.startswith(url)
        menu.append({"titulo": titulo, "url": url, "activo": activo})
    # El negocio se consulta solo si la plantilla lo usa (el panel no lo usa).
    return {"negocio": SimpleLazyObject(Negocio.cargar), "menu": menu}
