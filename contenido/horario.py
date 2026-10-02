"""Horario de atención en texto, como se muestra en la página: "Lunes a sábado · 9 a. m. a 1 p. m."."""

from itertools import groupby

DIAS = {1: "lunes", 2: "martes", 3: "miércoles", 4: "jueves", 5: "viernes", 6: "sábado", 7: "domingo"}


def hora_texto(hora):
    """9:00 → "9 a. m."; 14:30 → "2:30 p. m."; 12:00 → "12 m."."""
    if hora.hour == 12 and hora.minute == 0:
        return "12 m."
    doce = hora.hour % 12 or 12
    sufijo = "a. m." if hora.hour < 12 else "p. m."
    return f"{doce} {sufijo}" if hora.minute == 0 else f"{doce}:{hora.minute:02d} {sufijo}"


def dias_texto(dias):
    """[1..6] → "Lunes a sábado"; [6, 7] → "Sábado y domingo"; [3] → "Miércoles"."""
    if len(dias) == 1:
        texto = DIAS[dias[0]]
    elif len(dias) == 2:
        texto = f"{DIAS[dias[0]]} y {DIAS[dias[1]]}"
    else:
        texto = f"{DIAS[dias[0]]} a {DIAS[dias[-1]]}"
    return texto.capitalize()


def resumir_horario(franjas):
    """
    Agrupa los días seguidos que tienen el mismo horario.
    Devuelve [{"dias": "Lunes a sábado", "franjas": ["9 a. m. a 1 p. m.", "2 p. m. a 7 p. m."]}, ...];
    los días sin franjas salen con "franjas": [] (cerrado).
    """
    por_dia = {dia: [] for dia in DIAS}
    for franja in sorted(franjas, key=lambda f: (f.dia_semana, f.hora_apertura)):
        por_dia[franja.dia_semana].append(f"{hora_texto(franja.hora_apertura)} a {hora_texto(franja.hora_cierre)}")

    resumen = []
    for horas, grupo in groupby(DIAS, key=lambda dia: por_dia[dia]):
        dias = list(grupo)
        # Solo se juntan días consecutivos (groupby ya los recorre en orden de lunes a domingo).
        resumen.append({"dias": dias_texto(dias), "franjas": horas})
    return resumen
