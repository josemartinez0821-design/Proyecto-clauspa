"""
Fotos que sube la dueña desde el panel.

Se aceptan JPG, PNG o WebP de hasta 10 MB. Al guardarlas se enderezan (las fotos del
celular traen la rotación aparte), se reducen y se convierten a WebP, que pesa mucho menos.
Además se guardan copias más pequeñas (480, 960 y 1600 px de ancho) para que cada pantalla
descargue la que necesita (srcset). Cuando una foto se cambia o se borra, sus archivos se borran.
"""

from io import BytesIO
from pathlib import PurePosixPath

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.db import transaction
from django.db.models.signals import post_delete, pre_save
from django.utils.text import slugify
from PIL import Image, ImageOps

TAMANO_MAXIMO_MB = 10
ANCHOS = (480, 960, 1600)


def validar_tamano(archivo):
    # Solo se revisan las fotos recién subidas; las que ya están guardadas ya pasaron por aquí.
    if getattr(archivo, "_committed", True):
        return
    if archivo.size > TAMANO_MAXIMO_MB * 1024 * 1024:
        raise ValidationError(f"La foto pesa más de {TAMANO_MAXIMO_MB} MB. Elige una más liviana.")


VALIDADORES_FOTO = [
    FileExtensionValidator(["jpg", "jpeg", "png", "webp"], message="Sube la foto en formato JPG, PNG o WebP."),
    validar_tamano,
]


def nombre_variante(nombre, ancho):
    """Ejemplo: "servicios/limpieza.webp" → "servicios/limpieza-480.webp"."""
    ruta = PurePosixPath(nombre)
    return str(ruta.with_name(f"{ruta.stem}-{ancho}{ruta.suffix}"))


def _webp(imagen):
    salida = BytesIO()
    imagen.save(salida, "WEBP", quality=82, method=6)
    return ContentFile(salida.getvalue())


def guardar_variantes(storage, nombre, imagen, lado_maximo):
    """Guarda las copias más pequeñas de una foto ya convertida."""
    for ancho in ANCHOS:
        if ancho >= lado_maximo:
            continue
        copia = imagen
        if imagen.width > ancho:
            copia = imagen.resize((ancho, round(imagen.height * ancho / imagen.width)), Image.Resampling.LANCZOS)
        variante = nombre_variante(nombre, ancho)
        if storage.exists(variante):
            storage.delete(variante)
        storage.save(variante, _webp(copia))


def convertir_a_webp(campo, lado_maximo):
    """Si el campo trae una foto recién subida, la reduce a `lado_maximo` píxeles y la guarda en WebP."""
    if not campo or getattr(campo, "_committed", True):
        return

    imagen = ImageOps.exif_transpose(Image.open(campo))
    if imagen.mode not in ("RGB", "RGBA"):
        imagen = imagen.convert("RGBA" if imagen.mode in ("LA", "P", "PA") else "RGB")
    imagen.thumbnail((lado_maximo, lado_maximo), Image.Resampling.LANCZOS)

    nombre = (slugify(PurePosixPath(campo.name).stem) or "foto")[:60] + ".webp"
    campo.save(nombre, _webp(imagen), save=False)
    guardar_variantes(campo.storage, campo.name, imagen, lado_maximo)


def borrar_foto(storage, nombre):
    """Borra la foto y sus copias pequeñas."""
    for archivo in [nombre, *(nombre_variante(nombre, ancho) for ancho in ANCHOS)]:
        if storage.exists(archivo):
            storage.delete(archivo)


def limpiar_al_cambiar_o_borrar(modelo, campos):
    """
    Conecta las señales para que, si una foto se reemplaza, se quita o se borra su registro,
    sus archivos también se borren (después de confirmar la transacción, por si algo falla).
    """

    def al_guardar(sender, instance, raw=False, **kwargs):
        if raw or not instance.pk:
            return
        anterior = sender._default_manager.filter(pk=instance.pk).values(*campos).first()
        if not anterior:
            return
        for campo in campos:
            nombre_anterior, actual = anterior[campo], getattr(instance, campo)
            if nombre_anterior and nombre_anterior != actual.name:
                transaction.on_commit(lambda s=actual.storage, n=nombre_anterior: borrar_foto(s, n))

    def al_borrar(sender, instance, **kwargs):
        for campo in campos:
            archivo = getattr(instance, campo)
            if archivo:
                transaction.on_commit(lambda s=archivo.storage, n=archivo.name: borrar_foto(s, n))

    pre_save.connect(al_guardar, sender=modelo, weak=False, dispatch_uid=f"limpiar-guardar-{modelo.__name__}")
    post_delete.connect(al_borrar, sender=modelo, weak=False, dispatch_uid=f"limpiar-borrar-{modelo.__name__}")
