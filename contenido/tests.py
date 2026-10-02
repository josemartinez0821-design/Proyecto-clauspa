import shutil
import tempfile
from datetime import date, time
from io import BytesIO

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import inlineformset_factory
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from servicios.models import Servicio

from .admin import HorarioFormSet
from .models import Diapositiva, FotoLocal, HorarioAtencion, Negocio, solo_digitos

MEDIA_TEMPORAL = tempfile.mkdtemp()


def foto_png(ancho=3000, alto=2000):
    salida = BytesIO()
    Image.new("RGB", (ancho, alto), "#C749A7").save(salida, "PNG")
    return SimpleUploadedFile("Foto del Spa.png", salida.getvalue(), content_type="image/png")


@override_settings(MEDIA_ROOT=MEDIA_TEMPORAL)
class Fotos(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TEMPORAL, ignore_errors=True)

    def test_la_foto_se_reduce_y_se_guarda_en_webp(self):
        foto = FotoLocal.objects.create(negocio=Negocio.cargar(), imagen=foto_png(), texto_alternativo="Sala")
        self.assertTrue(foto.imagen.name.startswith("local/foto-del-spa"))
        self.assertTrue(foto.imagen.name.endswith(".webp"))
        with Image.open(foto.imagen.path) as imagen:
            self.assertEqual(imagen.format, "WEBP")
            self.assertEqual(imagen.size, (1600, 1067))

    def test_guardar_otra_vez_no_vuelve_a_convertir(self):
        foto = FotoLocal.objects.create(negocio=Negocio.cargar(), imagen=foto_png(), texto_alternativo="Sala")
        nombre = foto.imagen.name
        foto.texto_alternativo = "Sala de espera"
        foto.save()
        self.assertEqual(foto.imagen.name, nombre)


class DatosDelNegocio(TestCase):
    def test_hay_una_sola_fila(self):
        self.assertEqual(Negocio.cargar().pk, 1)
        Negocio(nombre="Otro").save()
        self.assertEqual(Negocio.objects.count(), 1)

    def test_los_numeros_se_guardan_solo_con_digitos(self):
        self.assertEqual(solo_digitos("+57 300 123 4567"), "3001234567")
        self.assertEqual(solo_digitos("300-123-4567"), "3001234567")
        negocio = Negocio.cargar()
        negocio.whatsapp = "300 123 4567"
        negocio.full_clean()
        self.assertEqual(negocio.whatsapp, "3001234567")

    def test_el_whatsapp_debe_ser_un_celular(self):
        negocio = Negocio.cargar()
        negocio.whatsapp = "601 234 5678"
        with self.assertRaises(ValidationError):
            negocio.full_clean()


class Horario(TestCase):
    def formset(self, franjas):
        FormSet = inlineformset_factory(Negocio, HorarioAtencion, formset=HorarioFormSet, fields="__all__", extra=0)
        datos = {"horarios-TOTAL_FORMS": len(franjas), "horarios-INITIAL_FORMS": 0}
        for i, (dia, abre, cierra) in enumerate(franjas):
            datos.update({f"horarios-{i}-dia_semana": dia, f"horarios-{i}-hora_apertura": abre,
                          f"horarios-{i}-hora_cierre": cierra})
        return FormSet(data=datos, instance=Negocio.cargar(), prefix="horarios")

    def test_manana_y_tarde_el_mismo_dia(self):
        self.assertTrue(self.formset([(1, "09:00", "13:00"), (1, "14:00", "19:00")]).is_valid())

    def test_franjas_que_se_cruzan(self):
        formset = self.formset([(1, "09:00", "13:00"), (1, "12:00", "19:00")])
        self.assertFalse(formset.is_valid())
        self.assertIn("El lunes tiene dos franjas que se cruzan.", formset.non_form_errors())

    def test_el_cierre_debe_ser_despues_de_la_apertura(self):
        franja = HorarioAtencion(negocio=Negocio.cargar(), dia_semana=1, hora_apertura=time(14), hora_cierre=time(9))
        with self.assertRaises(ValidationError):
            franja.full_clean()


class Slider(TestCase):
    def diapositiva(self, **cambios):
        datos = {"imagen": "slider/x.webp", "titulo": "Promo", "destino": Diapositiva.Destino.WHATSAPP}
        datos.update(cambios)
        return Diapositiva(**datos)

    def test_maximo_cuatro_activas(self):
        for _ in range(4):
            self.diapositiva().save()
        with self.assertRaises(ValidationError) as error:
            self.diapositiva().full_clean()
        self.assertIn("activa", error.exception.message_dict)
        self.diapositiva(activa=False).full_clean()

    def test_no_se_puede_desactivar_la_unica_activa(self):
        unica = self.diapositiva()
        unica.save()
        unica.activa = False
        with self.assertRaises(ValidationError):
            unica.full_clean()

    def test_si_lleva_a_un_servicio_hay_que_elegirlo(self):
        with self.assertRaises(ValidationError) as error:
            self.diapositiva(destino=Diapositiva.Destino.SERVICIO).full_clean()
        self.assertIn("servicio", error.exception.message_dict)

    def test_la_fecha_final_no_puede_ser_anterior(self):
        with self.assertRaises(ValidationError):
            self.diapositiva(fecha_inicio=date(2026, 12, 10), fecha_fin=date(2026, 12, 1)).full_clean()


class Panel(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("prueba", "prueba@ejemplo.com", "x"))

    def test_todas_las_secciones_abren(self):
        Servicio.objects.create(
            nombre="Masaje", slug="masaje", categoria="corporal", descripcion_breve="b", descripcion="d",
            duracion_min=50, duracion_max=60, precio=70000,
        )
        for nombre in ("servicios_servicio", "contenido_diapositiva", "contenido_tecnologia",
                       "contenido_preguntafrecuente", "auth_user"):
            for vista in ("changelist", "add"):
                respuesta = self.client.get(reverse(f"admin:{nombre}_{vista}"))
                self.assertEqual(respuesta.status_code, 200, f"{nombre} {vista}")
        respuesta = self.client.get(reverse("admin:servicios_servicio_change", args=[1]))
        self.assertContains(respuesta, "Cuidados")

    def test_negocio_y_nosotros_abren_directo_el_formulario(self):
        for nombre in ("contenido_negocio", "contenido_nosotros"):
            respuesta = self.client.get(reverse(f"admin:{nombre}_changelist"), follow=True)
            self.assertEqual(respuesta.status_code, 200)
            self.assertEqual(respuesta.redirect_chain[-1][0], reverse(f"admin:{nombre}_change", args=[1]))

    def test_inicio_del_panel(self):
        respuesta = self.client.get(reverse("admin:index"))
        self.assertContains(respuesta, "Accesos rápidos")
        self.assertContains(respuesta, "0 de 4")

    def test_textos_de_unfold_en_espanol(self):
        self.client.logout()
        respuesta = self.client.get(reverse("admin:login"))
        self.assertContains(respuesta, "Te damos la bienvenida a")
        self.assertContains(respuesta, "Volver a la página")
