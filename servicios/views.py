"""Páginas de servicios: Faciales, Corporales y el detalle de cada servicio."""

from django.shortcuts import get_object_or_404, redirect, render

from .models import Servicio

CATEGORIAS = {
    Servicio.Categoria.FACIAL: ("Faciales", "Tratamientos para limpiar, regenerar e hidratar tu rostro."),
    Servicio.Categoria.CORPORAL: ("Corporales", "Masajes, láser y tratamientos para tu cuerpo."),
}


def visibles():
    return Servicio.objects.filter(visible=True).prefetch_related("fotos")


def categoria(request, categoria):
    titulo, texto = CATEGORIAS[categoria]
    servicios = visibles().filter(categoria=categoria)
    return render(request, "sitio/categoria.html", {"titulo": titulo, "texto": texto, "servicios": servicios})


def detalle(request, categoria, slug):
    servicio = get_object_or_404(visibles(), slug=slug)
    if servicio.categoria != categoria:
        # Si llegan con la categoría equivocada (por ejemplo /corporales/limpieza…/), van a la dirección correcta.
        return redirect(servicio, permanent=True)
    relacionados = visibles().filter(categoria=categoria).exclude(pk=servicio.pk)[:3]
    return render(
        request,
        "sitio/detalle.html",
        {
            "servicio": servicio,
            "seccion": CATEGORIAS[categoria][0],
            "seccion_url": "faciales" if categoria == Servicio.Categoria.FACIAL else "corporales",
            "relacionados": relacionados,
            "nota_despues": "Además, te damos indicaciones personalizadas según "
            + ("tu tipo de piel." if categoria == Servicio.Categoria.FACIAL else "tu caso."),
        },
    )
