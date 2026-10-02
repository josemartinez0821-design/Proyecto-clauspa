"""
Crea las copias pequeñas (480, 960 y 1600 px) de las fotos que no las tengan.

Las fotos nuevas ya las traen; esto sirve para las que se subieron antes de que existiera esta función.
Se puede correr las veces que se quiera: solo trabaja con las que les falta alguna copia.
"""

from django.core.management.base import BaseCommand
from PIL import Image

from contenido.imagenes import ANCHOS, guardar_variantes, nombre_variante
from contenido.models import Diapositiva, FotoLocal, Negocio, Tecnologia
from servicios.models import FotoServicio

# (modelo, campo, lado máximo con que se guarda la foto)
FOTOS = [
    (FotoServicio, "imagen", 1600),
    (Diapositiva, "imagen", 2400),
    (FotoLocal, "imagen", 1600),
    (Tecnologia, "foto", 1200),
    (Negocio, "foto_duena", 1200),
    (Negocio, "logo", 800),
]


class Command(BaseCommand):
    help = "Crea las copias pequeñas de las fotos que todavía no las tienen."

    def handle(self, *args, **options):
        creadas = 0
        for modelo, campo, lado_maximo in FOTOS:
            for objeto in modelo.objects.exclude(**{campo: ""}):
                archivo = getattr(objeto, campo)
                faltan = [a for a in ANCHOS if a < lado_maximo and not archivo.storage.exists(nombre_variante(archivo.name, a))]
                if not faltan or not archivo.storage.exists(archivo.name):
                    continue
                with archivo.open("rb") as abierto, Image.open(abierto) as imagen:
                    imagen.load()
                    guardar_variantes(archivo.storage, archivo.name, imagen, lado_maximo)
                creadas += 1
        self.stdout.write(self.style.SUCCESS(f"Fotos con copias nuevas: {creadas}"))
