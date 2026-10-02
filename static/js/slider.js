// Slider de Inicio con Swiper (requisito S-02): cambia solo cada 6 segundos con un fundido suave,
// se detiene con el mouse encima o con el botón de pausa, y se puede deslizar con el dedo.
// Con una sola diapositiva no se mueve; si la persona pidió "reducir movimiento", no avanza solo.
document.addEventListener("DOMContentLoaded", () => {
  const elemento = document.querySelector(".slider");
  if (!elemento) return;

  const varias = elemento.querySelectorAll(".swiper-slide").length > 1;
  const reducir = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const avanzaSolo = varias && !reducir;

  const slider = new Swiper(elemento, {
    effect: "fade",
    fadeEffect: { crossFade: true },
    speed: reducir ? 0 : 900,
    rewind: varias,
    allowTouchMove: varias,
    autoplay: avanzaSolo ? { delay: 6000, pauseOnMouseEnter: true, disableOnInteraction: false } : false,
    pagination: { el: ".slider-puntos", clickable: true, bulletElement: "button" },
    navigation: { prevEl: ".slider-ant", nextEl: ".slider-sig" },
    keyboard: { enabled: true, onlyInViewport: true },
    a11y: {
      prevSlideMessage: "Diapositiva anterior",
      nextSlideMessage: "Diapositiva siguiente",
      firstSlideMessage: "Es la primera diapositiva",
      lastSlideMessage: "Es la última diapositiva",
      paginationBulletMessage: "Ir a la diapositiva {{index}}",
      slideLabelMessage: "{{index}} de {{slidesLength}}",
      containerRoleDescriptionMessage: "carrusel",
      itemRoleDescriptionMessage: "diapositiva",
    },
  });

  const pausa = elemento.querySelector(".slider-pausa");
  if (!pausa) return;
  if (!avanzaSolo) {
    pausa.hidden = true;
    return;
  }
  pausa.addEventListener("click", () => {
    const pausar = slider.autoplay.running;
    if (pausar) slider.autoplay.stop();
    else slider.autoplay.start();
    pausa.setAttribute("aria-label", pausar ? "Reanudar el carrusel" : "Pausar el carrusel");
    pausa.querySelector("use").setAttribute("href", pausar ? "#i-play" : "#i-pausa");
  });
});
