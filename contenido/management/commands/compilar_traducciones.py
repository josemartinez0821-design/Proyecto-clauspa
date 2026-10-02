"""
Compila los .po de locale/ a .mo sin GNU gettext.

`compilemessages` de Django necesita el programa msgfmt, que no viene con Windows.
Este comando entiende lo que usa el proyecto: comentarios, msgid y msgstr (también en varias líneas).
"""

import ast
import struct
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


def leer_po(ruta):
    mensajes = {}
    actual, clave = {}, None

    def guardar():
        # Un msgstr vacío significa "sin traducir", salvo en la cabecera (msgid "").
        if "msgid" in actual and (actual.get("msgstr") or actual["msgid"] == ""):
            mensajes[actual["msgid"]] = actual["msgstr"]

    for numero, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), start=1):
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        if linea.startswith("msgid "):
            guardar()
            actual, clave, linea = {}, "msgid", linea[6:]
        elif linea.startswith("msgstr "):
            clave, linea = "msgstr", linea[7:]
        if clave is None or not linea.startswith('"'):
            raise CommandError(f"{ruta.name}, línea {numero}: no se entiende «{linea}».")
        actual[clave] = actual.get(clave, "") + ast.literal_eval(linea)
    guardar()
    return mensajes


def escribir_mo(mensajes, ruta):
    """Formato .mo de GNU: cabecera, tabla de originales, tabla de traducciones y los textos."""
    pares = sorted((k.encode(), v.encode()) for k, v in mensajes.items())
    n = len(pares)
    inicio_originales = 7 * 4
    inicio_traducciones = inicio_originales + n * 8
    inicio_textos = inicio_traducciones + n * 8

    tabla_originales, tabla_traducciones, textos = [], [], b""
    for original, _ in pares:
        tabla_originales += [len(original), inicio_textos + len(textos)]
        textos += original + b"\0"
    for _, traduccion in pares:
        tabla_traducciones += [len(traduccion), inicio_textos + len(textos)]
        textos += traduccion + b"\0"

    cabecera = struct.pack("<7I", 0x950412DE, 0, n, inicio_originales, inicio_traducciones, 0, 0)
    tablas = struct.pack(f"<{4 * n}I", *tabla_originales, *tabla_traducciones)
    ruta.write_bytes(cabecera + tablas + textos)


class Command(BaseCommand):
    help = "Compila las traducciones de locale/ (.po → .mo) sin necesitar GNU gettext."

    def handle(self, *args, **options):
        for carpeta in settings.LOCALE_PATHS:
            for po in sorted(Path(carpeta).rglob("*.po")):
                mensajes = leer_po(po)
                escribir_mo(mensajes, po.with_suffix(".mo"))
                textos = sum(1 for clave in mensajes if clave)
                self.stdout.write(f"{po.relative_to(settings.BASE_DIR)}: {textos} textos compilados")
