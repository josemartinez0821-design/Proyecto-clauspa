import json
import re
import shutil
import tempfile
from datetime import date, time, timedelta
from io import BytesIO, StringIO
from pathlib import Path

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import CommandError, call_command
from django.forms import inlineformset_factory
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from PIL import Image

from servicios.models import FotoServicio, Servicio
from servicios.templatetags.spa import _variantes_existentes, srcset

from .admin import HorarioFormSet
from .horario import hora_texto, resumir_horario
from .imagenes import nombre_variante
from .models import Diapositiva, FotoLocal, HorarioAtencion, Negocio, PreguntaFrecuente, Tecnologia, solo_digitos


def foto_png(ancho=3000, alto=2000):
    salida = BytesIO()
    Image.new("RGB", (ancho, alto), "#C749A7").save(salida, "PNG")
    return SimpleUploadedFile("Foto del Spa.png", salida.getvalue(), content_type="image/png")


class ConMediaTemporal(TestCase):
    """Las fotos de estas pruebas se guardan en una carpeta temporal que se borra al terminar."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        carpeta = tempfile.mkdtemp()
        cls.enterClassContext(override_settings(MEDIA_ROOT=carpeta))
        cls.addClassCleanup(shutil.rmtree, carpeta, True)


class Fotos(ConMediaTemporal):
    def setUp(self):
        _variantes_existentes.clear()  # cada prueba revisa el disco de nuevo

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

    def test_se_guardan_copias_pequenas_para_cada_pantalla(self):
        foto = FotoLocal.objects.create(negocio=Negocio.cargar(), imagen=foto_png(), texto_alternativo="Sala")
        for ancho in (480, 960):
            with Image.open(foto.imagen.storage.path(nombre_variante(foto.imagen.name, ancho))) as copia:
                self.assertEqual(copia.width, ancho)
        # Con lado máximo 1600, la copia de 1600 no hace falta: la foto principal ya mide eso.
        self.assertFalse(foto.imagen.storage.exists(nombre_variante(foto.imagen.name, 1600)))
        self.assertEqual(
            srcset(foto.imagen, 1600),
            f"{foto.imagen.url[:-5]}-480.webp 480w, {foto.imagen.url[:-5]}-960.webp 960w, {foto.imagen.url} 1600w",
        )

    def test_srcset_no_usa_copias_que_no_existen(self):
        foto = FotoLocal.objects.create(negocio=Negocio.cargar(), imagen=foto_png(), texto_alternativo="Sala")
        foto.imagen.storage.delete(nombre_variante(foto.imagen.name, 480))
        self.assertNotIn("-480.webp", srcset(foto.imagen, 1600))
        self.assertIn("-960.webp 960w", srcset(foto.imagen, 1600))

    def test_al_cambiar_o_borrar_una_foto_se_borran_sus_archivos(self):
        foto = FotoLocal.objects.create(negocio=Negocio.cargar(), imagen=foto_png(), texto_alternativo="Sala")
        storage, primera = foto.imagen.storage, foto.imagen.name
        with self.captureOnCommitCallbacks(execute=True):
            foto.imagen = foto_png(800, 600)
            foto.save()
        self.assertFalse(storage.exists(primera))
        self.assertFalse(storage.exists(nombre_variante(primera, 480)))
        segunda = foto.imagen.name
        self.assertTrue(storage.exists(segunda))
        with self.captureOnCommitCallbacks(execute=True):
            foto.delete()
        self.assertFalse(storage.exists(segunda))
        self.assertFalse(storage.exists(nombre_variante(segunda, 480)))

    def test_generar_tamanos_completa_las_copias_que_falten(self):
        foto = FotoLocal.objects.create(negocio=Negocio.cargar(), imagen=foto_png(), texto_alternativo="Sala")
        copia = nombre_variante(foto.imagen.name, 960)
        foto.imagen.storage.delete(copia)
        call_command("generar_tamanos", stdout=StringIO())
        self.assertTrue(foto.imagen.storage.exists(copia))


@override_settings(DEBUG=True)
class DatosDeEjemplo(ConMediaTemporal):
    def test_carga_todo_y_se_puede_repetir_sin_duplicar(self):
        call_command("cargar_ejemplos", stdout=StringIO())
        call_command("cargar_ejemplos", stdout=StringIO())

        self.assertEqual(Servicio.objects.count(), 8)
        self.assertEqual(FotoServicio.objects.count(), 8)
        self.assertEqual(Servicio.objects.filter(destacado=True).count(), 4)
        self.assertEqual(Servicio.objects.filter(es_combo=True).count(), 2)
        self.assertEqual(Diapositiva.objects.count(), 4)
        self.assertEqual(Diapositiva.objects.filter(activa=True).count(), 3)
        self.assertEqual(Tecnologia.objects.count(), 3)
        self.assertEqual(PreguntaFrecuente.objects.count(), 5)
        negocio = Negocio.cargar()
        self.assertEqual(negocio.horarios.count(), 12)
        self.assertEqual(negocio.fotos_local.count(), 3)

    def test_los_datos_cumplen_las_reglas_del_panel(self):
        call_command("cargar_ejemplos", stdout=StringIO())
        for servicio in Servicio.objects.all():
            servicio.full_clean()
            self.assertTrue(servicio.cuidados_antes and servicio.cuidados_despues and servicio.consultar_antes)
        for diapositiva in Diapositiva.objects.all():
            diapositiva.full_clean()
            self.assertTrue(diapositiva.imagen.name.endswith(".webp"))
        for franja in HorarioAtencion.objects.all():
            franja.full_clean()

    def test_fotos_de_referencia_desde_una_carpeta(self):
        carpeta = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, carpeta, True)
        for archivo in ("servicios/masaje-relajante.jpg", "servicios/masaje-relajante-2.jpg", "slider/1.jpg"):
            (carpeta / archivo).parent.mkdir(exist_ok=True)
            Image.new("RGB", (1200, 800), "#5D7FCD").save(carpeta / archivo, "JPEG")
        call_command("cargar_ejemplos", fotos=carpeta, stdout=StringIO())
        masaje = Servicio.objects.get(slug="masaje-relajante")
        self.assertEqual(masaje.fotos.count(), 2)
        self.assertIn("foto de referencia", masaje.fotos.first().texto_alternativo)
        self.assertEqual(Servicio.objects.get(slug="depilacion-laser").fotos.count(), 1)  # sin foto real: la generada
        self.assertTrue(Diapositiva.objects.get(orden=1).imagen.name.startswith("slider/tu-piel-renovada"))

    @override_settings(DEBUG=False)
    def test_no_se_carga_en_el_servidor(self):
        with self.assertRaises(CommandError):
            call_command("cargar_ejemplos", stdout=StringIO())


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


class HorarioEnTexto(TestCase):
    def franja(self, dia, abre, cierra):
        return HorarioAtencion(dia_semana=dia, hora_apertura=time(*abre), hora_cierre=time(*cierra))

    def test_horas_como_se_dicen_en_colombia(self):
        self.assertEqual(hora_texto(time(9)), "9 a. m.")
        self.assertEqual(hora_texto(time(14, 30)), "2:30 p. m.")
        self.assertEqual(hora_texto(time(12)), "12 m.")
        self.assertEqual(hora_texto(time(0, 15)), "12:15 a. m.")

    def test_junta_los_dias_seguidos_con_el_mismo_horario(self):
        franjas = [self.franja(d, (9,), (13,)) for d in range(1, 7)] + [self.franja(d, (14,), (19,)) for d in range(1, 7)]
        self.assertEqual(
            resumir_horario(franjas),
            [
                {"dias": "Lunes a sábado", "franjas": ["9 a. m. a 1 p. m.", "2 p. m. a 7 p. m."]},
                {"dias": "Domingo", "franjas": []},
            ],
        )

    def test_dias_distintos_quedan_aparte(self):
        franjas = [self.franja(d, (9,), (19,)) for d in range(1, 6)] + [self.franja(6, (9,), (13,))]
        resumen = resumir_horario(franjas)
        self.assertEqual([grupo["dias"] for grupo in resumen], ["Lunes a viernes", "Sábado", "Domingo"])
        self.assertEqual(resumen[1]["franjas"], ["9 a. m. a 1 p. m."])


class EnlacesDelNegocio(TestCase):
    def test_whatsapp_con_numero_y_mensaje(self):
        negocio = Negocio(whatsapp="3001234567")
        self.assertEqual(
            negocio.enlace_whatsapp("Hola, quiero una cita para Masaje relajante."),
            "https://wa.me/573001234567?text=Hola%2C%20quiero%20una%20cita%20para%20Masaje%20relajante.",
        )

    def test_sin_numero_whatsapp_deja_elegir_el_chat(self):
        self.assertTrue(Negocio().enlace_whatsapp().startswith("https://wa.me/?text=Hola"))

    def test_telefono_y_nombre(self):
        negocio = Negocio(telefono="6012345678")
        self.assertEqual(negocio.enlace_telefono, "tel:+576012345678")
        self.assertEqual(negocio.telefono_visible, "601 234 5678")
        self.assertEqual(negocio.partes_nombre, ("Claudia", "Spa"))


class SitioPublico(TestCase):
    PAGINAS = ("inicio", "faciales", "corporales", "nosotros", "contacto", "privacidad")

    def test_todas_las_paginas_tienen_encabezado_pie_y_whatsapp(self):
        for nombre in self.PAGINAS:
            respuesta = self.client.get(reverse(nombre))
            self.assertEqual(respuesta.status_code, 200, nombre)
            self.assertContains(respuesta, "Relajación y belleza")
            self.assertContains(respuesta, "Aviso de privacidad")
            self.assertContains(respuesta, 'aria-label="Escribir por WhatsApp"')

    def test_el_menu_marca_la_pagina_actual(self):
        respuesta = self.client.get(reverse("corporales"))
        self.assertContains(respuesta, 'aria-current="page"', count=2)  # menú del computador y del celular
        self.assertRegex(respuesta.content.decode(), r'href="/corporales/"[^>]*\n?\s*aria-current="page"')

    def test_el_pie_muestra_el_horario(self):
        negocio = Negocio.cargar()
        negocio.horarios.create(dia_semana=1, hora_apertura=time(9), hora_cierre=time(13))
        respuesta = self.client.get(reverse("contacto"))
        self.assertContains(respuesta, "Lunes")
        self.assertContains(respuesta, "9 a. m. a 1 p. m.")


def crear_servicio(**cambios):
    datos = {"nombre": "Masaje relajante", "slug": "masaje-relajante", "categoria": "corporal",
             "descripcion_breve": "Breve.", "descripcion": "Texto.", "duracion_min": 50, "duracion_max": 60,
             "precio": 70000}
    datos.update(cambios)
    return Servicio.objects.create(**datos)


class PaginaDeInicio(TestCase):
    def diapositiva(self, titulo, **cambios):
        datos = {"imagen": "slider/x.webp", "titulo": titulo, "destino": Diapositiva.Destino.CONTACTO}
        datos.update(cambios)
        return Diapositiva.objects.create(**datos)

    def test_el_slider_muestra_solo_las_vigentes(self):
        hoy = timezone.localdate()
        self.diapositiva("Siempre")
        self.diapositiva("Desactivada", activa=False)
        self.diapositiva("Ya pasó", fecha_inicio=hoy - timedelta(days=10), fecha_fin=hoy - timedelta(days=1))
        self.diapositiva("Todavía no", fecha_inicio=hoy + timedelta(days=1))
        self.diapositiva("Este mes", fecha_inicio=hoy, fecha_fin=hoy)
        respuesta = self.client.get(reverse("inicio"))
        self.assertEqual([d.titulo for d in respuesta.context["diapositivas"]], ["Siempre", "Este mes"])

    def test_destacados_y_tecnologia(self):
        crear_servicio(destacado=True)
        crear_servicio(nombre="Depilación láser", slug="depilacion-laser")
        Tecnologia.objects.create(nombre="Hidrafacial", descripcion="Limpia.")
        Tecnologia.objects.create(nombre="Equipo oculto", descripcion="No sale.", visible=False)
        respuesta = self.client.get(reverse("inicio"))
        self.assertContains(respuesta, "Masaje relajante")
        self.assertNotContains(respuesta, "Depilación láser")
        self.assertContains(respuesta, 'id="tecnologia"')
        self.assertNotContains(respuesta, "Equipo oculto")

    def test_a_donde_lleva_el_boton_de_cada_diapositiva(self):
        masaje = crear_servicio()
        con_servicio = self.diapositiva("A", destino=Diapositiva.Destino.SERVICIO, servicio=masaje)
        self.assertEqual(con_servicio.enlace, "/corporales/masaje-relajante/")
        masaje.visible = False
        masaje.save()
        con_servicio.refresh_from_db()
        self.assertEqual(con_servicio.enlace, "")  # servicio oculto: la diapositiva queda sin botón
        self.assertEqual(self.diapositiva("B", destino=Diapositiva.Destino.TECNOLOGIA).enlace, "/#tecnologia")
        self.assertEqual(self.diapositiva("C", destino=Diapositiva.Destino.FACIALES).enlace, "/faciales/")
        self.assertTrue(self.diapositiva("D", destino=Diapositiva.Destino.WHATSAPP).enlace.startswith("https://wa.me/"))


class OtrasPaginas(TestCase):
    def test_contacto_muestra_las_preguntas_visibles(self):
        PreguntaFrecuente.objects.create(pregunta="¿Cómo pido una cita?", respuesta="Por WhatsApp.")
        PreguntaFrecuente.objects.create(pregunta="Pregunta oculta", respuesta="No.", visible=False)
        respuesta = self.client.get(reverse("contacto"))
        self.assertContains(respuesta, "¿Cómo pido una cita?")
        self.assertNotContains(respuesta, "Pregunta oculta")

    def test_el_mapa_solo_aparece_con_la_ciudad(self):
        negocio = Negocio.cargar()
        negocio.direccion, negocio.barrio = "Carrera 9 # 9A-21", "Canadá"
        negocio.save()
        self.assertNotContains(self.client.get(reverse("contacto")), "<iframe")
        negocio.ciudad = "Pueblo"
        negocio.save()
        respuesta = self.client.get(reverse("contacto"))
        self.assertContains(respuesta, "<iframe")
        self.assertContains(respuesta, "Carrera%209%20%23%209A-21%2C%20Barrio%20Canad%C3%A1%2C%20Pueblo%2C%20Colombia")

    def test_nosotros_muestra_los_anios_de_experiencia(self):
        negocio = Negocio.cargar()
        negocio.texto_nosotros, negocio.anios_experiencia = "Nuestra historia.", 15
        negocio.save()
        respuesta = self.client.get(reverse("nosotros"))
        self.assertContains(respuesta, "15+")
        self.assertContains(respuesta, "Nuestra historia.")

    def test_pagina_no_encontrada(self):
        respuesta = self.client.get("/esta-pagina-no-existe/")
        self.assertEqual(respuesta.status_code, 404)
        self.assertContains(respuesta, "No encontramos esta página", status_code=404)
        self.assertContains(respuesta, "Volver al inicio", status_code=404)


class Buscadores(TestCase):
    """Lo que leen Google y las redes cuando alguien comparte la página."""

    def test_cada_pagina_tiene_su_titulo_y_descripcion(self):
        crear_servicio()
        casos = {
            reverse("inicio"): "<title>Claudia Spa · Relajación y belleza</title>",
            reverse("faciales"): "<title>Faciales · Claudia Spa</title>",
            "/corporales/masaje-relajante/": "<title>Masaje relajante · Claudia Spa</title>",
            reverse("contacto"): "<title>Contacto · Claudia Spa</title>",
        }
        for url, titulo in casos.items():
            respuesta = self.client.get(url)
            self.assertContains(respuesta, titulo, html=False)
            self.assertContains(respuesta, f'<link rel="canonical" href="http://testserver{url}">')
            self.assertContains(respuesta, '<meta property="og:image"')
        self.assertContains(self.client.get("/corporales/masaje-relajante/"), 'content="Breve. Aprox. 50 a 60 min. $70.000."')

    def test_datos_del_negocio_para_google(self):
        negocio = Negocio.cargar()
        negocio.direccion, negocio.barrio, negocio.telefono = "Carrera 9 # 9A-21", "Canadá", "3001234567"
        negocio.save()
        negocio.horarios.create(dia_semana=6, hora_apertura=time(9), hora_cierre=time(13))
        respuesta = self.client.get(reverse("contacto")).content.decode()
        datos = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', respuesta).group(1))
        self.assertEqual(datos["@type"], "DaySpa")
        self.assertEqual(datos["telephone"], "+573001234567")
        self.assertEqual(datos["address"]["streetAddress"], "Carrera 9 # 9A-21, Barrio Canadá")
        self.assertEqual(datos["openingHoursSpecification"][0]["dayOfWeek"], "https://schema.org/Saturday")

    def test_un_texto_del_panel_no_puede_romper_los_datos(self):
        negocio = Negocio.cargar()
        negocio.lema = "</script><script>alert(1)</script>"
        negocio.save()
        self.assertNotContains(self.client.get(reverse("inicio")), "</script><script>alert(1)")

    def test_mapa_del_sitio_y_robots(self):
        crear_servicio()
        crear_servicio(nombre="Oculto", slug="oculto", visible=False)
        mapa = self.client.get("/sitemap.xml").content.decode()
        self.assertIn("http://testserver/corporales/masaje-relajante/", mapa)
        self.assertIn("http://testserver/contacto/", mapa)
        self.assertNotIn("oculto", mapa)
        robots = self.client.get("/robots.txt").content.decode()
        self.assertIn("Disallow: /panel/", robots)
        self.assertIn("Sitemap: http://testserver/sitemap.xml", robots)

    def test_las_letras_salen_del_propio_sitio(self):
        respuesta = self.client.get(reverse("inicio"))
        self.assertNotContains(respuesta, "fonts.googleapis.com")
        self.assertContains(respuesta, "/static/fonts/jost-latin-400-normal.woff2")

    def test_la_pagina_no_encontrada_no_se_indexa(self):
        self.assertContains(self.client.get("/no-existe/"), '<meta name="robots" content="noindex">', status_code=404)


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
        masaje = Servicio.objects.create(
            nombre="Masaje", slug="masaje", categoria="corporal", descripcion_breve="b", descripcion="d",
            duracion_min=50, duracion_max=60, precio=70000,
        )
        for nombre in ("servicios_servicio", "contenido_diapositiva", "contenido_tecnologia",
                       "contenido_preguntafrecuente", "auth_user"):
            for vista in ("changelist", "add"):
                respuesta = self.client.get(reverse(f"admin:{nombre}_{vista}"))
                self.assertEqual(respuesta.status_code, 200, f"{nombre} {vista}")
        respuesta = self.client.get(reverse("admin:servicios_servicio_change", args=[masaje.pk]))
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
