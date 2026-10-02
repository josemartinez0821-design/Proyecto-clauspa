"""Formulario de servicios del panel."""

import re

from django import forms
from unfold.widgets import UnfoldAdminTextInputWidget

from .models import Servicio


class CampoPesos(forms.IntegerField):
    """Precio en pesos: acepta 90000, 90.000 o $ 90.000 y lo muestra con puntos de miles."""

    def __init__(self, **kwargs):
        kwargs.setdefault("min_value", 0)
        kwargs["widget"] = UnfoldAdminTextInputWidget(attrs={"prefix": "$", "inputmode": "numeric"})
        super().__init__(**kwargs)

    def to_python(self, value):
        if isinstance(value, str):
            value = re.sub(r"[$\s.,]", "", value)
        return super().to_python(value)

    def prepare_value(self, value):
        if isinstance(value, int):
            return f"{value:,}".replace(",", ".")
        return value


def campo_minutos():
    return UnfoldAdminTextInputWidget(attrs={"suffix": "min", "inputmode": "numeric"})


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = "__all__"
        field_classes = {"precio": CampoPesos, "precio_anterior": CampoPesos}
        widgets = {"duracion_min": campo_minutos(), "duracion_max": campo_minutos()}
