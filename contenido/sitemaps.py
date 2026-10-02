"""Mapa del sitio (sitemap.xml) para Google: las páginas fijas y cada servicio visible."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from servicios.models import Servicio


class PaginasSitemap(Sitemap):
    def items(self):
        return ["inicio", "faciales", "corporales", "nosotros", "contacto", "privacidad"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return {"inicio": 1.0, "privacidad": 0.2}.get(item, 0.7)


class ServiciosSitemap(Sitemap):
    priority = 0.8

    def items(self):
        return Servicio.objects.filter(visible=True)

    def lastmod(self, servicio):
        return servicio.actualizado


SITEMAPS = {"paginas": PaginasSitemap, "servicios": ServiciosSitemap}
