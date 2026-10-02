"""Contenido general de la página: datos del negocio, horario, slider, tecnología, preguntas y fotos del spa."""

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F, Q

from .imagenes import VALIDADORES_FOTO, convertir_a_webp


def solo_digitos(numero):
    """Deja solo los dígitos de un número colombiano: "+57 300 123 4567" → "3001234567"."""
    digitos = re.sub(r"\D", "", numero)
    if len(digitos) == 12 and digitos.startswith("57"):
        digitos = digitos[2:]
    return digitos


validar_celular = RegexValidator(r"^3\d{9}$", "Escribe los 10 dígitos del celular. Ejemplo: 300 123 4567.")
validar_telefono = RegexValidator(
    r"^\d{10}$", "Escribe los 10 dígitos del número (los fijos llevan el indicativo, por ejemplo 601 234 5678)."
)


class Negocio(models.Model):
    """Datos del spa. Hay una sola fila (id 1); se obtiene con `Negocio.cargar()`."""

    # Nombre y logo
    nombre = models.CharField("nombre", max_length=80, default="Claudia Spa")
    lema = models.CharField("lema", max_length=80, default="Relajación y belleza")
    logo = models.ImageField("logo", upload_to="negocio/", blank=True, validators=VALIDADORES_FOTO)

    # Contacto
    whatsapp = models.CharField("WhatsApp", max_length=20, blank=True, validators=[validar_celular])
    telefono = models.CharField(
        "teléfono", max_length=20, blank=True, validators=[validar_telefono], help_text="Para el botón Llamar."
    )
    saludo_whatsapp = models.CharField(
        "saludo del botón de WhatsApp",
        max_length=200,
        default="Hola, vi la página de Claudia Spa y quiero pedir información.",
        help_text="Mensaje que ya va escrito cuando la persona toca el botón flotante de WhatsApp.",
    )

    # Dirección
    direccion = models.CharField("dirección", max_length=120, blank=True)
    barrio = models.CharField("barrio", max_length=60, blank=True)
    ciudad = models.CharField("ciudad", max_length=60, blank=True)
    enlace_mapa = models.URLField(
        "enlace de Google Maps", blank=True, help_text="En Google Maps: Compartir → Copiar vínculo."
    )

    # Redes y reseñas
    instagram = models.URLField("Instagram", blank=True)
    facebook = models.URLField("Facebook", blank=True)
    tiktok = models.URLField("TikTok", blank=True)
    enlace_resenas = models.URLField("enlace a las reseñas de Google", blank=True)

    # Página Nosotros
    titulo_nosotros = models.CharField("título", max_length=100, default="Nuestra historia")
    texto_nosotros = models.TextField(
        "texto", blank=True, help_text="Tu historia y tu experiencia. Deja una línea en blanco entre párrafos."
    )
    foto_duena = models.ImageField(
        "tu foto", upload_to="negocio/", blank=True, validators=VALIDADORES_FOTO
    )

    actualizado = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        db_table = "negocio"
        verbose_name = "datos del negocio"
        verbose_name_plural = "datos del negocio"

    def __str__(self):
        return self.nombre

    @classmethod
    def cargar(cls):
        negocio, _ = cls.objects.get_or_create(pk=1)
        return negocio

    def clean_fields(self, exclude=None):
        # Se aceptan números con espacios, guiones o +57; se guardan solo los 10 dígitos.
        self.whatsapp = solo_digitos(self.whatsapp)
        self.telefono = solo_digitos(self.telefono)
        super().clean_fields(exclude)

    def save(self, *args, **kwargs):
        self.pk = 1
        convertir_a_webp(self.logo, 800)
        convertir_a_webp(self.foto_duena, 1200)
        super().save(*args, **kwargs)


class Nosotros(Negocio):
    """La parte de Negocio que se edita en la sección Nosotros del panel (es la misma fila)."""

    class Meta:
        proxy = True
        verbose_name = "Nosotros"
        verbose_name_plural = "Nosotros"


class HorarioAtencion(models.Model):
    """Una franja de atención. Un día puede tener dos (mañana y tarde); un día sin franjas está cerrado."""

    class Dia(models.IntegerChoices):
        LUNES = 1, "Lunes"
        MARTES = 2, "Martes"
        MIERCOLES = 3, "Miércoles"
        JUEVES = 4, "Jueves"
        VIERNES = 5, "Viernes"
        SABADO = 6, "Sábado"
        DOMINGO = 7, "Domingo"

    negocio = models.ForeignKey(Negocio, models.CASCADE, related_name="horarios", verbose_name="negocio")
    dia_semana = models.PositiveSmallIntegerField("día", choices=Dia)
    hora_apertura = models.TimeField("abre a las")
    hora_cierre = models.TimeField("cierra a las")

    class Meta:
        db_table = "horario_atencion"
        ordering = ["dia_semana", "hora_apertura"]
        verbose_name = "franja de atención"
        verbose_name_plural = "horario de atención"
        constraints = [
            models.CheckConstraint(
                condition=Q(hora_cierre__gt=F("hora_apertura")),
                name="horario_cierre_despues_de_apertura",
                violation_error_message="La hora de cierre debe ser después de la de apertura.",
            ),
        ]

    def __str__(self):
        return f"{self.get_dia_semana_display()} de {self.hora_apertura:%H:%M} a {self.hora_cierre:%H:%M}"

    def clean(self):
        if self.hora_apertura and self.hora_cierre and self.hora_cierre <= self.hora_apertura:
            raise ValidationError({"hora_cierre": "Debe ser después de la hora en que abre."})


class Diapositiva(models.Model):
    """Una diapositiva del slider de Inicio. Puede haber de 1 a 4 activas."""

    MAXIMO_ACTIVAS = 4

    class Destino(models.TextChoices):
        SERVICIO = "servicio", "Un servicio"
        FACIALES = "faciales", "Página de Faciales"
        CORPORALES = "corporales", "Página de Corporales"
        WHATSAPP = "whatsapp", "WhatsApp"
        CONTACTO = "contacto", "Página de Contacto"
        TECNOLOGIA = "tecnologia", "Sección de Tecnología"

    imagen = models.ImageField(
        "imagen",
        upload_to="slider/",
        validators=VALIDADORES_FOTO,
        help_text="Horizontal y de buena calidad (al menos 1600 píxeles de ancho).",
    )
    antetitulo = models.CharField(
        "texto pequeño sobre el título", max_length=40, blank=True, help_text="Opcional. Ejemplo: Promoción del mes."
    )
    titulo = models.CharField("título", max_length=80)
    texto = models.CharField("texto corto", max_length=160, blank=True)
    texto_boton = models.CharField("texto del botón", max_length=30, default="Ver más")
    destino = models.CharField("el botón lleva a", max_length=12, choices=Destino, default=Destino.SERVICIO)
    servicio = models.ForeignKey(
        "servicios.Servicio",
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="diapositivas",
        verbose_name="servicio",
        help_text="Solo si el botón lleva a un servicio.",
    )
    activa = models.BooleanField("activa", default=True)
    orden = models.PositiveIntegerField("orden", default=0)
    fecha_inicio = models.DateField(
        "mostrar desde", null=True, blank=True, help_text="Opcional, para promociones con fecha."
    )
    fecha_fin = models.DateField("mostrar hasta", null=True, blank=True, help_text="Opcional. Ese día todavía se muestra.")

    class Meta:
        db_table = "diapositiva"
        ordering = ["orden", "id"]
        verbose_name = "diapositiva"
        verbose_name_plural = "diapositivas"
        constraints = [
            models.CheckConstraint(
                condition=Q(fecha_inicio__isnull=True) | Q(fecha_fin__isnull=True) | Q(fecha_fin__gte=F("fecha_inicio")),
                name="diapositiva_fechas_validas",
                violation_error_message="La fecha final no puede ser anterior a la inicial.",
            ),
        ]

    def __str__(self):
        return self.titulo

    def clean(self):
        errores = {}
        if self.destino == self.Destino.SERVICIO and not self.servicio_id:
            errores["servicio"] = "Elige el servicio al que lleva el botón."
        if self.fecha_inicio and self.fecha_fin and self.fecha_fin < self.fecha_inicio:
            errores["fecha_fin"] = "No puede ser anterior a la fecha de inicio."

        otras_activas = Diapositiva.objects.filter(activa=True).exclude(pk=self.pk)
        if self.activa and otras_activas.count() >= self.MAXIMO_ACTIVAS:
            errores["activa"] = (
                f"Ya hay {self.MAXIMO_ACTIVAS} diapositivas activas, que es el máximo. Desactiva otra primero."
            )
        elif not self.activa and self.es_la_unica_activa():
            errores["activa"] = "Es la única diapositiva activa y el slider de Inicio quedaría vacío. Activa otra primero."
        if errores:
            raise ValidationError(errores)

    def es_la_unica_activa(self):
        if not self.pk:
            return False
        activas = Diapositiva.objects.filter(activa=True)
        return activas.filter(pk=self.pk).exists() and not activas.exclude(pk=self.pk).exists()

    def save(self, *args, **kwargs):
        convertir_a_webp(self.imagen, 2400)
        super().save(*args, **kwargs)


class Tecnologia(models.Model):
    """Un equipo de la sección Tecnología de Inicio (hidrafacial, máscara LED, aparatología…)."""

    nombre = models.CharField("nombre", max_length=80)
    descripcion = models.TextField("para qué sirve", max_length=400, help_text="Dos o tres líneas.")
    foto = models.ImageField("foto", upload_to="tecnologia/", blank=True, validators=VALIDADORES_FOTO)
    visible = models.BooleanField("visible en la página", default=True)
    orden = models.PositiveIntegerField("orden", default=0)

    class Meta:
        db_table = "tecnologia"
        ordering = ["orden", "id"]
        verbose_name = "equipo"
        verbose_name_plural = "tecnología"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        convertir_a_webp(self.foto, 1200)
        super().save(*args, **kwargs)


class PreguntaFrecuente(models.Model):
    pregunta = models.CharField("pregunta", max_length=200)
    respuesta = models.TextField("respuesta")
    visible = models.BooleanField("visible en la página", default=True)
    orden = models.PositiveIntegerField("orden", default=0)

    class Meta:
        db_table = "pregunta_frecuente"
        ordering = ["orden", "id"]
        verbose_name = "pregunta frecuente"
        verbose_name_plural = "preguntas frecuentes"

    def __str__(self):
        return self.pregunta


class FotoLocal(models.Model):
    """Fotos del spa que se muestran en Nosotros."""

    negocio = models.ForeignKey(Negocio, models.CASCADE, related_name="fotos_local", verbose_name="negocio")
    imagen = models.ImageField("foto", upload_to="local/", validators=VALIDADORES_FOTO)
    texto_alternativo = models.CharField(
        "qué se ve en la foto",
        max_length=150,
        help_text="Una frase corta. La leen Google y las personas que usan lector de pantalla.",
    )
    orden = models.PositiveIntegerField("orden", default=0)

    class Meta:
        db_table = "foto_local"
        ordering = ["orden", "id"]
        verbose_name = "foto del spa"
        verbose_name_plural = "fotos del spa"

    def __str__(self):
        return self.texto_alternativo

    def save(self, *args, **kwargs):
        convertir_a_webp(self.imagen, 1600)
        super().save(*args, **kwargs)
