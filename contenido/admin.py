"""Secciones del panel: Slider, Tecnología, Preguntas frecuentes, Nosotros, Datos del negocio y usuarios."""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as GroupAdminBase
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, PaginationInlineFormSet, UserChangeForm, UserCreationForm
from unfold.widgets import UnfoldAdminTextareaWidget

from .models import Diapositiva, FotoLocal, HorarioAtencion, Negocio, Nosotros, PreguntaFrecuente, Tecnologia

TEXTOS_CORTOS = {models.TextField: {"widget": UnfoldAdminTextareaWidget(attrs={"rows": 4})}}


def miniatura(campo, alto=40, ancho=64):
    if not campo:
        return "—"
    return format_html(
        '<img src="{}" alt="" style="height:{}px;width:{}px;object-fit:cover;border-radius:6px">',
        campo.url,
        alto,
        ancho,
    )


class UnaSolaFilaAdmin(ModelAdmin):
    """Para Negocio y Nosotros: no hay lista; la sección abre directo el formulario de la única fila."""

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        negocio = Negocio.cargar()
        return redirect(reverse(f"admin:{self.opts.app_label}_{self.opts.model_name}_change", args=[negocio.pk]))


# Datos del negocio


class HorarioFormSet(PaginationInlineFormSet):
    def clean(self):
        super().clean()
        franjas = {}
        for formulario in self.forms:
            datos = getattr(formulario, "cleaned_data", None)
            if not datos or datos.get("DELETE") or not datos.get("hora_apertura") or not datos.get("hora_cierre"):
                continue
            franjas.setdefault(datos["dia_semana"], []).append((datos["hora_apertura"], datos["hora_cierre"]))
        for dia, horas in franjas.items():
            horas.sort()
            for (_, cierre), (apertura, _) in zip(horas, horas[1:]):
                if apertura < cierre:
                    nombre = HorarioAtencion.Dia(dia).label
                    raise ValidationError(f"El {nombre.lower()} tiene dos franjas que se cruzan.")


class HorarioInline(TabularInline):
    model = HorarioAtencion
    formset = HorarioFormSet
    fields = ("dia_semana", "hora_apertura", "hora_cierre")
    extra = 0
    tab = True


@admin.register(Negocio)
class NegocioAdmin(UnaSolaFilaAdmin):
    inlines = [HorarioInline]
    warn_unsaved_form = True
    fieldsets = (
        ("Contacto", {"classes": ["tab"], "fields": ("whatsapp", "telefono", "saludo_whatsapp")}),
        ("Dirección", {"classes": ["tab"], "fields": ("direccion", "barrio", "ciudad", "enlace_mapa")}),
        ("Redes sociales", {"classes": ["tab"], "fields": ("instagram", "facebook", "tiktok", "enlace_resenas")}),
        ("Nombre y logo", {"classes": ["tab"], "fields": ("nombre", "lema", "logo")}),
    )


# Nosotros


class FotoLocalInline(TabularInline):
    model = FotoLocal
    fields = ("imagen", "texto_alternativo", "orden")
    extra = 0
    ordering_field = "orden"
    hide_ordering_field = True


@admin.register(Nosotros)
class NosotrosAdmin(UnaSolaFilaAdmin):
    fields = ("titulo_nosotros", "texto_nosotros", "foto_duena", "anios_experiencia")
    inlines = [FotoLocalInline]
    warn_unsaved_form = True
    formfield_overrides = {models.TextField: {"widget": UnfoldAdminTextareaWidget(attrs={"rows": 8})}}


# Slider


@admin.register(Diapositiva)
class DiapositivaAdmin(ModelAdmin):
    list_display = ("imagen_miniatura", "titulo", "boton", "activa", "cuando")
    list_display_links = ("imagen_miniatura", "titulo")
    ordering_field = "orden"
    hide_ordering_field = True
    warn_unsaved_form = True
    actions = None
    fieldsets = (
        (None, {"fields": ("imagen", "antetitulo", "titulo", "texto")}),
        ("Botón", {"fields": ("texto_boton", "destino", "servicio")}),
        ("Cuándo se muestra", {"fields": ("activa", ("fecha_inicio", "fecha_fin"))}),
    )

    def has_delete_permission(self, request, obj=None):
        if obj and obj.es_la_unica_activa():
            return False
        return super().has_delete_permission(request, obj)

    @display(description="imagen")
    def imagen_miniatura(self, diapositiva):
        return miniatura(diapositiva.imagen)

    @display(description="botón")
    def boton(self, diapositiva):
        if diapositiva.destino == Diapositiva.Destino.SERVICIO and diapositiva.servicio:
            return f"{diapositiva.texto_boton} → {diapositiva.servicio}"
        return f"{diapositiva.texto_boton} → {diapositiva.get_destino_display()}"

    @display(description="se muestra")
    def cuando(self, diapositiva):
        inicio, fin = diapositiva.fecha_inicio, diapositiva.fecha_fin
        if inicio and fin:
            return f"Del {inicio:%d/%m/%Y} al {fin:%d/%m/%Y}"
        if inicio:
            return f"Desde el {inicio:%d/%m/%Y}"
        if fin:
            return f"Hasta el {fin:%d/%m/%Y}"
        return "Siempre"


# Tecnología y preguntas frecuentes


@admin.register(Tecnologia)
class TecnologiaAdmin(ModelAdmin):
    list_display = ("foto_miniatura", "nombre", "visible")
    list_display_links = ("foto_miniatura", "nombre")
    ordering_field = "orden"
    hide_ordering_field = True
    fields = ("nombre", "descripcion", "foto", "visible")
    formfield_overrides = TEXTOS_CORTOS

    @display(description="foto")
    def foto_miniatura(self, equipo):
        return miniatura(equipo.foto)


@admin.register(PreguntaFrecuente)
class PreguntaFrecuenteAdmin(ModelAdmin):
    list_display = ("pregunta", "visible")
    ordering_field = "orden"
    hide_ordering_field = True
    search_fields = ("pregunta", "respuesta")
    fields = ("pregunta", "respuesta", "visible")
    formfield_overrides = TEXTOS_CORTOS


# Usuarios del panel: los de Django, con el diseño de Unfold.

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UsuarioAdmin(UserAdminBase, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GrupoAdmin(GroupAdminBase, ModelAdmin):
    pass
