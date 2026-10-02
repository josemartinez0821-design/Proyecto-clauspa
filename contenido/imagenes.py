"""
Fotos que sube la dueña desde el panel.

Se aceptan JPG, PNG o WebP de hasta 10 MB. Al guardarlas se enderezan (las fotos del
celular traen la rotación aparte), se reducen y se convierten a WebP, que pesa mucho menos.
"""

from io import BytesIO
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from PIL import Image, ImageOps

TAMANO_MAXIMO_MB = 10


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


def convertir_a_webp(campo, lado_maximo):
    """Si el campo trae una foto recién subida, la reduce a `lado_maximo` píxeles y la guarda en WebP."""
    if not campo or getattr(campo, "_committed", True):
        return

    imagen = ImageOps.exif_transpose(Image.open(campo))
    if imagen.mode not in ("RGB", "RGBA"):
        imagen = imagen.convert("RGBA" if imagen.mode in ("LA", "P", "PA") else "RGB")
    imagen.thumbnail((lado_maximo, lado_maximo), Image.Resampling.LANCZOS)

    salida = BytesIO()
    imagen.save(salida, "WEBP", quality=82, method=6)
    nombre = (slugify(Path(campo.name).stem) or "foto")[:60] + ".webp"
    campo.save(nombre, ContentFile(salida.getvalue()), save=False)
