"""Sección Servicios del panel."""

from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from unfold.widgets import UnfoldAdminTextareaWidget

from .forms import ServicioForm
from .models import FotoServicio, Servicio


class FotoServicioInline(TabularInline):
    model = FotoServicio
    fields = ("imagen", "texto_alternativo", "orden")
    extra = 0
    ordering_field = "orden"
    hide_ordering_field = True
    tab = True


@admin.register(Servicio)
class ServicioAdmin(ModelAdmin):
    form = ServicioForm
    inlines = [FotoServicioInline]
    list_display = ("nombre", "categoria", "duracion", "precio_completo", "visible", "destacado")
    list_filter = ("categoria", "visible", "destacado", "es_combo")
    search_fields = ("nombre",)
    ordering_field = "orden"
    hide_ordering_field = True
    prepopulated_fields = {"slug": ("nombre",)}
    warn_unsaved_form = True
    formfield_overrides = {models.TextField: {"widget": UnfoldAdminTextareaWidget(attrs={"rows": 5})}}
    fieldsets = (
        (
            "Datos básicos",
            {
                "classes": ["tab"],
                "fields": ("nombre", "slug", "categoria", "es_combo", "descripcion_breve", "visible", "destacado"),
            },
        ),
        (
            "Descripción",
            {"classes": ["tab"], "fields": ("descripcion", "ideal_para", "que_incluye", "recomendaciones")},
        ),
        (
            "Cuidados",
            {"classes": ["tab"], "fields": ("cuidados_antes", "cuidados_despues", "consultar_antes")},
        ),
        (
            "Precio y duración",
            {
                "classes": ["tab"],
                "fields": (
                    ("duracion_min", "duracion_max"),
                    "duracion_por_sesion",
                    "tipo_precio",
                    "precio",
                    "sufijo_precio",
                    "precio_anterior",
                ),
            },
        ),
    )

    @display(description="duración", ordering="duracion_min")
    def duracion(self, servicio):
        return servicio.duracion_texto

    @display(description="precio", ordering="precio")
    def precio_completo(self, servicio):
        return f"{servicio.precio_texto} {servicio.sufijo_precio}".strip()
