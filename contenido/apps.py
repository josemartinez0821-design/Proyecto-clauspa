from django.apps import AppConfig


class ContenidoConfig(AppConfig):
    name = "contenido"
    verbose_name = "Contenido de la página"

    def ready(self):
        from servicios.models import FotoServicio

        from .imagenes import limpiar_al_cambiar_o_borrar
        from .models import Diapositiva, FotoLocal, Negocio, Nosotros, Tecnologia

        # Al cambiar o borrar una foto, se borran sus archivos (y sus copias pequeñas).
        limpiar_al_cambiar_o_borrar(FotoServicio, ["imagen"])
        limpiar_al_cambiar_o_borrar(Diapositiva, ["imagen"])
        limpiar_al_cambiar_o_borrar(FotoLocal, ["imagen"])
        limpiar_al_cambiar_o_borrar(Tecnologia, ["foto"])
        limpiar_al_cambiar_o_borrar(Negocio, ["logo", "foto_duena"])
        limpiar_al_cambiar_o_borrar(Nosotros, ["logo", "foto_duena"])  # la sección Nosotros guarda como "Nosotros"
