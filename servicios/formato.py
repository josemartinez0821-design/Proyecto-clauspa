"""Cómo se escriben precios y duraciones en la página y en el panel."""


def pesos(valor):
    """90000 → "$90.000"."""
    return "$" + f"{valor:,}".replace(",", ".")


def tiempo(minutos):
    """45 → "45 min"; 120 → "2 h"; 150 → "2 h 30 min"."""
    horas, resto = divmod(minutos, 60)
    if not horas:
        return f"{resto} min"
    return f"{horas} h {resto} min" if resto else f"{horas} h"


def duracion(minima, maxima, por_sesion=False):
    """
    Duración aproximada: "45 a 60 min"; desde 2 horas, en horas: "2 h a 2 h 30 min".
    La palabra "Aprox." la pone la plantilla.
    """
    if maxima < 120:
        texto = f"{minima} min" if minima == maxima else f"{minima} a {maxima} min"
    else:
        texto = tiempo(minima) if minima == maxima else f"{tiempo(minima)} a {tiempo(maxima)}"
    return f"{texto} por sesión" if por_sesion else texto
