"""
Carga los datos de ejemplo (contenido/ejemplos.py) para ver la página completa en el PC.

Se puede correr varias veces: actualiza los textos sin duplicar nada y solo crea fotos donde no hay.
Las fotos son imágenes generadas aquí mismo con los colores del logo y dicen "Foto de ejemplo".
"""

import calendar
from datetime import time
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image, ImageColor, ImageDraw, ImageFont

from contenido import ejemplos
from contenido.models import Diapositiva, Negocio, PreguntaFrecuente, Tecnologia
from servicios.models import Servicio

# Degradados (arriba, abajo) con los colores del logo
COLORES = {
    "facial": ("#C749A7", "#5E1D4C"),
    "corporal": ("#4F8F1C", "#2F5C0D"),
    "slider": ("#A83A8C", "#2A1F27"),
    "local": ("#5D7FCD", "#3F63B5"),
}


def fuente(tamano):
    """Una letra del sistema con tildes (la que trae Pillow no las tiene, y "láser" saldría con un cuadro)."""
    for nombre in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(nombre, tamano)
        except OSError:
            continue
    return ImageFont.load_default(size=tamano)


def foto_de_ejemplo(colores, ancho, alto, titulo=None):
    """PNG con un degradado y la marca "Foto de ejemplo" (con el título en el centro, si se da)."""
    arriba, abajo = (ImageColor.getrgb(color) for color in colores)
    mascara = Image.linear_gradient("L").resize((ancho, alto))
    imagen = Image.composite(Image.new("RGB", (ancho, alto), abajo), Image.new("RGB", (ancho, alto), arriba), mascara)
    dibujo = ImageDraw.Draw(imagen, "RGBA")
    for x, y, radio in ((0.85, 0.15, 0.45), (0.1, 0.95, 0.35)):
        r = radio * alto
        dibujo.ellipse((x * ancho - r, y * alto - r, x * ancho + r, y * alto + r), fill=(255, 255, 255, 20))

    pequena = fuente(max(alto // 24, 14))
    if titulo:
        # El texto cabe en el cuadrado del centro: el detalle del servicio muestra la foto recortada en cuadrado.
        tamano = alto // 12
        while tamano > 16 and dibujo.textlength(titulo, font=fuente(tamano)) > min(ancho, alto) * 0.85:
            tamano -= 2
        dibujo.text((ancho / 2, alto / 2), titulo, font=fuente(tamano), anchor="ms", fill=(255, 255, 255, 240))
        dibujo.text((ancho / 2, alto / 2 + alto // 20), "Foto de ejemplo", font=pequena, anchor="ma",
                    fill=(255, 255, 255, 190))
    else:
        # Arriba a la derecha: abajo quedan los controles del slider.
        dibujo.text((ancho - alto // 20, alto // 20), "Foto de ejemplo", font=pequena, anchor="ra",
                    fill=(255, 255, 255, 170))

    salida = BytesIO()
    imagen.save(salida, "PNG")
    return ContentFile(salida.getvalue(), name=f"{slugify(titulo or 'diapositiva')}.png")


def foto_de_carpeta(ruta):
    return ContentFile(ruta.read_bytes(), name=ruta.name)


class Command(BaseCommand):
    help = "Carga los datos de ejemplo de Claudia Spa (solo en el PC de desarrollo)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fotos",
            type=Path,
            help="Carpeta con fotos de referencia que reemplazan a las generadas: servicios/<slug>.jpg "
            "(y <slug>-2.jpg…), slider/<número>.jpg y local/<número>.jpg. No se suben al repositorio.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Los datos de ejemplo son solo para el PC de desarrollo (DEBUG=True).")
        self.carpeta = options.get("fotos")
        if self.carpeta and not self.carpeta.is_dir():
            raise CommandError(f"No existe la carpeta de fotos: {self.carpeta}")
        with transaction.atomic():
            self.servicios()
            self.diapositivas()
            self.tecnologia_y_preguntas()
            self.negocio()
        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados."))

    def servicios(self):
        for orden, datos in enumerate(ejemplos.SERVICIOS, start=1):
            datos = dict(datos)
            servicio, _ = Servicio.objects.update_or_create(slug=datos.pop("slug"), defaults={**datos, "orden": orden})
            reales = self.buscar("servicios", f"{servicio.slug}.jpg", f"{servicio.slug}-[0-9].jpg")
            if reales:
                servicio.fotos.all().delete()  # sus archivos se borran solos (contenido/imagenes.py)
                for numero, ruta in enumerate(reales):
                    servicio.fotos.create(
                        imagen=foto_de_carpeta(ruta), texto_alternativo=f"{servicio.nombre} (foto de referencia)", orden=numero
                    )
            elif not servicio.fotos.exists():
                servicio.fotos.create(
                    imagen=foto_de_ejemplo(COLORES[servicio.categoria], 1600, 1200, servicio.nombre),
                    texto_alternativo=f"{servicio.nombre} (foto de ejemplo)",
                )
        self.stdout.write(f"Servicios: {Servicio.objects.count()}")

    def diapositivas(self):
        hoy = timezone.localdate()
        for orden, datos in enumerate(ejemplos.DIAPOSITIVAS, start=1):
            datos = dict(datos)
            slug = datos.pop("servicio", None)
            datos["servicio"] = Servicio.objects.get(slug=slug) if slug else None
            if datos.pop("este_mes", False):
                ultimo_dia = calendar.monthrange(hoy.year, hoy.month)[1]
                datos["fecha_inicio"], datos["fecha_fin"] = hoy.replace(day=1), hoy.replace(day=ultimo_dia)
            diapositiva, _ = Diapositiva.objects.update_or_create(
                titulo=datos.pop("titulo"), defaults={**datos, "orden": orden}
            )
            real = self.buscar("slider", f"{orden}.jpg")
            if real:
                diapositiva.imagen = ContentFile(real[0].read_bytes(), name=f"{slugify(diapositiva.titulo)}.jpg")
                diapositiva.save()
            elif not diapositiva.imagen:
                diapositiva.imagen = foto_de_ejemplo(COLORES["slider"], 2400, 1000)
                diapositiva.save()
        activas = Diapositiva.objects.filter(activa=True).count()
        self.stdout.write(f"Diapositivas: {Diapositiva.objects.count()} ({activas} activas)")

    def tecnologia_y_preguntas(self):
        for orden, (nombre, descripcion) in enumerate(ejemplos.TECNOLOGIA, start=1):
            Tecnologia.objects.update_or_create(nombre=nombre, defaults={"descripcion": descripcion, "orden": orden})
        for orden, (pregunta, respuesta) in enumerate(ejemplos.PREGUNTAS, start=1):
            PreguntaFrecuente.objects.update_or_create(
                pregunta=pregunta, defaults={"respuesta": respuesta, "orden": orden}
            )
        self.stdout.write(f"Tecnología: {Tecnologia.objects.count()} · Preguntas: {PreguntaFrecuente.objects.count()}")

    def negocio(self):
        negocio = Negocio.cargar()
        if not negocio.texto_nosotros:
            negocio.titulo_nosotros = ejemplos.NOSOTROS_TITULO
            negocio.texto_nosotros = ejemplos.NOSOTROS_TEXTO
            negocio.save()
        if negocio.anios_experiencia is None:
            negocio.anios_experiencia = ejemplos.NOSOTROS_ANIOS
            negocio.save()
        if not negocio.horarios.exists():
            for dia, abre, cierra in ejemplos.HORARIO:
                negocio.horarios.create(
                    dia_semana=dia, hora_apertura=time.fromisoformat(abre), hora_cierre=time.fromisoformat(cierra)
                )
        reales = self.buscar("local", *(f"{numero}.jpg" for numero in range(1, len(ejemplos.FOTOS_LOCAL) + 1)))
        if reales:
            negocio.fotos_local.all().delete()
            for orden, (ruta, descripcion) in enumerate(zip(reales, ejemplos.FOTOS_LOCAL), start=1):
                negocio.fotos_local.create(
                    imagen=foto_de_carpeta(ruta), texto_alternativo=f"{descripcion} (foto de referencia)", orden=orden
                )
        elif not negocio.fotos_local.exists():
            for orden, descripcion in enumerate(ejemplos.FOTOS_LOCAL, start=1):
                negocio.fotos_local.create(
                    imagen=foto_de_ejemplo(COLORES["local"], 1600, 1200, descripcion),
                    texto_alternativo=f"{descripcion} (foto de ejemplo)",
                    orden=orden,
                )
        self.stdout.write(
            f"Horario: {negocio.horarios.count()} franjas · Fotos del spa: {negocio.fotos_local.count()}"
        )

    def buscar(self, subcarpeta, *patrones):
        """Fotos de la carpeta --fotos que coinciden con los patrones, en orden (vacío si no se dio carpeta)."""
        if not self.carpeta:
            return []
        encontradas = []
        for patron in patrones:
            encontradas += sorted((self.carpeta / subcarpeta).glob(patron))
        return encontradas
