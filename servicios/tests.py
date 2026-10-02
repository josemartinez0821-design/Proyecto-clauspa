from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .forms import CampoPesos
from .models import Servicio


def servicio(**cambios):
    datos = {
        "nombre": "Limpieza facial profunda",
        "slug": "limpieza-facial-profunda",
        "categoria": Servicio.Categoria.FACIAL,
        "descripcion_breve": "Limpieza completa.",
        "descripcion": "Texto.",
        "duracion_min": 75,
        "duracion_max": 90,
        "precio": 90000,
    }
    datos.update(cambios)
    return Servicio(**datos)


class ReglasDelServicio(TestCase):
    def test_un_servicio_correcto_pasa(self):
        servicio().full_clean()

    def test_la_duracion_maxima_no_puede_ser_menor(self):
        with self.assertRaises(ValidationError) as error:
            servicio(duracion_min=60, duracion_max=45).full_clean()
        self.assertIn("duracion_max", error.exception.message_dict)

    def test_misma_duracion_minima_y_maxima_se_permite(self):
        servicio(duracion_min=60, duracion_max=60).full_clean()

    def test_el_precio_anterior_debe_ser_mayor(self):
        with self.assertRaises(ValidationError) as error:
            servicio(precio=90000, precio_anterior=90000).full_clean()
        self.assertIn("precio_anterior", error.exception.message_dict)
        servicio(precio=240000, precio_anterior=270000).full_clean()

    def test_la_base_de_datos_tambien_cuida_las_reglas(self):
        with self.assertRaises(IntegrityError):
            servicio(duracion_min=60, duracion_max=30).save()


class PrecioEnPesos(TestCase):
    def test_acepta_puntos_y_signo_pesos(self):
        campo = CampoPesos()
        self.assertEqual(campo.clean("90.000"), 90000)
        self.assertEqual(campo.clean("$ 1.250.000"), 1250000)
        self.assertEqual(campo.clean("80000"), 80000)

    def test_rechaza_texto(self):
        with self.assertRaises(ValidationError):
            CampoPesos().clean("noventa mil")

    def test_muestra_el_precio_con_puntos(self):
        self.assertEqual(CampoPesos().prepare_value(90000), "90.000")


class ServicioDesdeElPanel(TestCase):
    def test_crear_un_servicio_escribiendo_el_precio_con_puntos(self):
        self.client.force_login(User.objects.create_superuser("prueba", "prueba@ejemplo.com", "x"))
        datos = {
            "nombre": "Masaje relajante",
            "slug": "masaje-relajante",
            "categoria": "corporal",
            "descripcion_breve": "Masaje de cuerpo completo.",
            "descripcion": "Texto.",
            "cuidados_antes": "Ven con ropa cómoda\nNo comas pesado antes",
            "duracion_min": "50",
            "duracion_max": "60",
            "precio": "$ 70.000",
            "tipo_precio": "fijo",
            "visible": "on",
            "fotos-TOTAL_FORMS": "0",
            "fotos-INITIAL_FORMS": "0",
        }
        respuesta = self.client.post(reverse("admin:servicios_servicio_add"), datos)
        self.assertEqual(respuesta.status_code, 302)
        guardado = Servicio.objects.get(slug="masaje-relajante")
        self.assertEqual(guardado.precio, 70000)
        self.assertEqual(guardado.cuidados_antes.splitlines(), ["Ven con ropa cómoda", "No comas pesado antes"])

        respuesta = self.client.get(reverse("admin:servicios_servicio_change", args=[guardado.pk]))
        self.assertContains(respuesta, 'value="70.000"')
