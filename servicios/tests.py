from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from contenido.models import Negocio

from .formato import duracion, pesos, tiempo
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


class Formatos(TestCase):
    def test_pesos(self):
        self.assertEqual(pesos(90000), "$90.000")
        self.assertEqual(pesos(1250000), "$1.250.000")

    def test_tiempo(self):
        self.assertEqual(tiempo(45), "45 min")
        self.assertEqual(tiempo(120), "2 h")
        self.assertEqual(tiempo(150), "2 h 30 min")

    def test_duracion_aproximada(self):
        self.assertEqual(duracion(45, 60), "45 a 60 min")
        self.assertEqual(duracion(60, 60), "60 min")
        self.assertEqual(duracion(120, 150), "2 h a 2 h 30 min")  # desde 2 horas, en horas
        self.assertEqual(duracion(15, 45, por_sesion=True), "15 a 45 min por sesión")

    def test_precio_del_servicio(self):
        self.assertEqual(servicio(precio=80000, tipo_precio="desde").precio_texto, "Desde $80.000")
        self.assertEqual(servicio().precio_texto, "$90.000")


class PaginasDeServicios(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.limpieza = servicio(
            descripcion="Primer párrafo.\r\n\r\nSegundo párrafo.",
            ideal_para="Piel grasa\nPiel opaca",
            que_incluye="Limpieza\nExtracción",
            cuidados_antes="Ven sin maquillaje",
            cuidados_despues="Usa bloqueador",
            consultar_antes="Estás en embarazo",
            recomendaciones="Cada 4 a 6 semanas.",
            orden=1,
        )
        cls.limpieza.save()
        cls.oculto = servicio(nombre="Oculto", slug="oculto", visible=False)
        cls.oculto.save()
        cls.masaje = servicio(nombre="Masaje", slug="masaje", categoria=Servicio.Categoria.CORPORAL)
        cls.masaje.save()
        for i in range(4):
            servicio(nombre=f"Facial {i}", slug=f"facial-{i}", orden=10 + i).save()

    def test_la_lista_muestra_solo_los_visibles_de_su_categoria(self):
        respuesta = self.client.get(reverse("faciales"))
        self.assertContains(respuesta, "Limpieza facial profunda")
        self.assertNotContains(respuesta, "Oculto")
        self.assertNotContains(respuesta, "Masaje")
        self.assertContains(respuesta, "Aprox. 75 a 90 min")

    def test_el_detalle_muestra_toda_la_informacion(self):
        respuesta = self.client.get(self.limpieza.get_absolute_url())
        self.assertEqual(self.limpieza.get_absolute_url(), "/faciales/limpieza-facial-profunda/")
        for texto in ("<p>Primer párrafo.</p>", "<p>Segundo párrafo.</p>", "Ideal para", "Piel opaca", "Qué incluye",
                      "Extracción", "Antes de tu cita", "Ven sin maquillaje", "Después de tu cita", "Usa bloqueador",
                      "según tu tipo de piel", "Avísanos antes si…", "Estás en embarazo", "Recomendaciones"):
            self.assertContains(respuesta, texto)

    def test_el_boton_de_whatsapp_lleva_el_nombre_del_servicio(self):
        respuesta = self.client.get(self.limpieza.get_absolute_url())
        mensaje = "Hola, vi la página de Claudia Spa y quiero pedir una cita para Limpieza facial profunda."
        self.assertContains(respuesta, Negocio.cargar().enlace_whatsapp(mensaje))

    def test_los_apartados_vacios_no_se_muestran(self):
        respuesta = self.client.get(self.masaje.get_absolute_url())
        for texto in ("Ideal para", "Qué incluye", "Antes de tu cita", "Avísanos antes si", "Recomendaciones"):
            self.assertNotContains(respuesta, texto)

    def test_llamar_solo_si_hay_telefono(self):
        self.assertNotContains(self.client.get(self.masaje.get_absolute_url()), "tel:")
        negocio = Negocio.cargar()
        negocio.telefono = "3001234567"
        negocio.save()
        self.assertContains(self.client.get(self.masaje.get_absolute_url()), 'href="tel:+573001234567"')

    def test_un_servicio_oculto_no_se_puede_ver(self):
        self.assertEqual(self.client.get("/faciales/oculto/").status_code, 404)

    def test_con_la_categoria_equivocada_redirige(self):
        respuesta = self.client.get("/corporales/limpieza-facial-profunda/")
        self.assertRedirects(respuesta, "/faciales/limpieza-facial-profunda/", status_code=301)

    def test_tambien_te_puede_interesar_maximo_tres(self):
        respuesta = self.client.get(self.limpieza.get_absolute_url())
        relacionados = list(respuesta.context["relacionados"])
        self.assertEqual(len(relacionados), 3)
        self.assertTrue(all(s.categoria == "facial" and s.visible and s != self.limpieza for s in relacionados))


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
