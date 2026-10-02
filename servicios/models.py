"""Servicios del spa (faciales y corporales) y sus fotos."""

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q
from django.urls import reverse

from contenido.imagenes import VALIDADORES_FOTO, convertir_a_webp

from .formato import duracion, pesos

MINUTOS = [MinValueValidator(5), MaxValueValidator(600)]


class Servicio(models.Model):
    class Categoria(models.TextChoices):
        FACIAL = "facial", "Facial"
        CORPORAL = "corporal", "Corporal"

    class TipoPrecio(models.TextChoices):
        FIJO = "fijo", "Fijo"
        DESDE = "desde", "Desde"

    # Datos básicos
    nombre = models.CharField("nombre", max_length=80, unique=True)
    slug = models.SlugField(
        "dirección web",
        max_length=90,
        unique=True,
        help_text="Se llena sola con el nombre. Es el final de la dirección de la página del servicio; "
        "mejor no cambiarla después de publicada.",
    )
    categoria = models.CharField("categoría", max_length=10, choices=Categoria)
    es_combo = models.BooleanField("es un combo", default=False, help_text="Muestra la etiqueta «Combo».")
    descripcion_breve = models.CharField(
        "descripción breve", max_length=160, help_text="Una o dos líneas. Se ve en la tarjeta del servicio."
    )

    # Lo que se lee en la página del servicio
    descripcion = models.TextField(
        "descripción completa",
        help_text="Qué es, para qué sirve y qué resultados esperar. Deja una línea en blanco entre párrafos.",
    )
    ideal_para = models.TextField(
        "ideal para",
        blank=True,
        help_text="Para quién es o qué mejora. Uno por línea. Ejemplo: Piel con puntos negros.",
    )
    que_incluye = models.TextField("qué incluye", blank=True, help_text="Los pasos del servicio, uno por línea.")
    recomendaciones = models.TextField(
        "recomendaciones", blank=True, help_text="Cada cuánto hacerlo, cuántas sesiones o con qué combinarlo."
    )

    # Cuidados: se muestran como "Antes de tu cita", "Después de tu cita" y "Avísanos antes si…"
    cuidados_antes = models.TextField(
        "cuidados antes de la cita", blank=True, help_text="Uno por línea. Ejemplo: Ven sin maquillaje."
    )
    cuidados_despues = models.TextField(
        "cuidados después de la cita",
        blank=True,
        help_text="Uno por línea. Ejemplo: Usa bloqueador solar todos los días.",
    )
    consultar_antes = models.TextField(
        "avísanos antes si…",
        blank=True,
        help_text="Casos en los que la persona debe contarte antes de pedir la cita. Uno por línea. "
        "Ejemplo: Estás en embarazo o lactancia.",
    )

    # Precio y duración (siempre aproximada)
    duracion_min = models.PositiveSmallIntegerField("duración mínima", validators=MINUTOS, help_text="En minutos.")
    duracion_max = models.PositiveSmallIntegerField(
        "duración máxima",
        validators=MINUTOS,
        help_text="En minutos. Si siempre dura lo mismo, escribe el mismo número.",
    )
    duracion_por_sesion = models.BooleanField(
        "la duración es por sesión",
        default=False,
        help_text="Márcalo en paquetes o planes de varias sesiones: se muestra «Aprox. 15 a 45 min por sesión».",
    )
    precio = models.PositiveIntegerField("precio", help_text="En pesos. Puedes escribirlo con o sin puntos.")
    tipo_precio = models.CharField(
        "tipo de precio",
        max_length=5,
        choices=TipoPrecio,
        default=TipoPrecio.FIJO,
        help_text="«Desde» se muestra así: Desde $80.000.",
    )
    precio_anterior = models.PositiveIntegerField(
        "precio anterior",
        null=True,
        blank=True,
        help_text="Opcional. Se muestra tachado para que se vea el ahorro.",
    )
    sufijo_precio = models.CharField(
        "texto después del precio", max_length=30, blank=True, help_text="Opcional. Ejemplo: por sesión."
    )

    # Dónde y cómo se muestra
    destacado = models.BooleanField("mostrar en Inicio", default=False)
    visible = models.BooleanField(
        "visible en la página", default=True, help_text="Desmárcalo para ocultar el servicio sin borrarlo."
    )
    orden = models.PositiveIntegerField("orden", default=0, db_index=True)
    creado = models.DateTimeField("creado", auto_now_add=True)
    actualizado = models.DateTimeField("actualizado", auto_now=True)

    class Meta:
        db_table = "servicio"
        ordering = ["orden", "nombre"]
        verbose_name = "servicio"
        verbose_name_plural = "servicios"
        constraints = [
            models.CheckConstraint(
                condition=Q(duracion_max__gte=F("duracion_min")),
                name="servicio_duracion_valida",
                violation_error_message="La duración máxima no puede ser menor que la mínima.",
            ),
            models.CheckConstraint(
                condition=Q(precio_anterior__isnull=True) | Q(precio_anterior__gt=F("precio")),
                name="servicio_precio_anterior_mayor",
                violation_error_message="El precio anterior debe ser mayor que el precio actual.",
            ),
        ]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse(f"detalle_{self.categoria}", args=[self.slug])

    @property
    def duracion_texto(self):
        return duracion(self.duracion_min, self.duracion_max, self.duracion_por_sesion)

    @property
    def precio_texto(self):
        """Precio principal: "$90.000" o "Desde $80.000" (el sufijo y el precio anterior van aparte)."""
        texto = pesos(self.precio)
        return f"Desde {texto}" if self.tipo_precio == self.TipoPrecio.DESDE else texto

    @property
    def foto_principal(self):
        """La primera foto (usa las fotos precargadas con prefetch_related si las hay)."""
        fotos = list(self.fotos.all())
        return fotos[0] if fotos else None

    def clean(self):
        errores = {}
        if self.duracion_min and self.duracion_max and self.duracion_max < self.duracion_min:
            errores["duracion_max"] = "No puede ser menor que la duración mínima."
        if self.precio_anterior is not None and self.precio is not None and self.precio_anterior <= self.precio:
            errores["precio_anterior"] = "Debe ser mayor que el precio actual; si no hay descuento, déjalo vacío."
        if errores:
            raise ValidationError(errores)


class FotoServicio(models.Model):
    servicio = models.ForeignKey(Servicio, models.CASCADE, related_name="fotos", verbose_name="servicio")
    imagen = models.ImageField("foto", upload_to="servicios/", validators=VALIDADORES_FOTO)
    texto_alternativo = models.CharField(
        "qué se ve en la foto",
        max_length=150,
        help_text="Una frase corta. La leen Google y las personas que usan lector de pantalla.",
    )
    orden = models.PositiveIntegerField("orden", default=0)

    class Meta:
        db_table = "foto_servicio"
        ordering = ["orden", "id"]
        verbose_name = "foto"
        verbose_name_plural = "fotos"

    def __str__(self):
        return self.texto_alternativo

    def save(self, *args, **kwargs):
        convertir_a_webp(self.imagen, 1600)
        super().save(*args, **kwargs)
