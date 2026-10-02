# Decisiones del proyecto Claudia Spa

Registro de lo decidido con el usuario (Jose Miguel, hijo de la dueña). Actualizado el 29/09/2026.

## Qué es

Página web **informativa** y **responsive** para **Claudia Spa**, el spa de la mamá del usuario, que **atiende sola**
(una sola agenda). Muestra lo que hace en **faciales y corporales**, con precios y toda la información; tiene un **panel**
para que ella cambie servicios, precios, fotos y textos sin ayuda. Las citas se piden por **WhatsApp** o por
**teléfono** (fase 1) y, desde la fase 2, con una **agenda en línea**.

## Registro de decisiones

| Fecha | Decisión |
|---|---|
| 27/09/2026 | Solo la parte del spa: sin relojes, ropa ni vestidos de baño |
| 27/09/2026 | Sin facturación ni DIAN |
| 27/09/2026 | Base de datos MariaDB |
| 27/09/2026 | Proyecto personal e individual: nada del SENA, sin las marcas de 2025 (TrustEdge, ClauSoft) |
| 28/09/2026 | Sin venta de productos: ni tienda ni vitrina |
| 28/09/2026 | Sitio responsive; servicios en dos categorías: faciales y corporales |
| 28/09/2026 | Citas por WhatsApp (mensaje ya escrito) y por teléfono (botón Llamar) |
| 28/09/2026 | Sin pagos en línea: la página muestra los precios y toda la información |
| 28/09/2026 | Duraciones siempre aproximadas ("Aprox. 45 a 60 min"), nunca exactas |
| 28/09/2026 | Inicio con un slider elegante de 1 a 4 diapositivas (servicios o promociones) |
| 28/09/2026 | Agenda en línea: sí, en la fase 2 |
| 29/09/2026 | Tecnología: Django + Tailwind CSS + MariaDB (el usuario solo conocía Java y quería aprender algo distinto) |
| 29/09/2026 | Reglas de la fase 2: máximo 30 días adelante, horas cada 30 min, 3 h para confirmar, domicilios fuera de la agenda en línea |
| 29/09/2026 | El nombre es **Claudia Spa** (no "Clau-Spa"); lema "Relajación y belleza" |
| 29/09/2026 | Sin fotos de diplomas; Nosotros lleva un texto breve con su experiencia |
| 29/09/2026 | Se quitan las tarjetas grandes de Faciales y Corporales en Inicio |
| 29/09/2026 | Cada opción del menú es su propio apartado (página), no una sola página larga |
| 29/09/2026 | Colores tomados del logo (ver "Diseño") |
| 29/09/2026 | Cuidados **antes y después** distintos para cada servicio (idea del usuario) |
| 29/09/2026 | Combos dentro de su categoría con etiqueta "Combo" y precio anterior tachado; también en el slider |
| 29/09/2026 | La recuperación de contraseña del panel llega al correo del hijo (la mamá no usa Gmail) |
| 29/09/2026 | Sección "Tecnología" en Inicio (hidrafacial, máscara LED, aparatología) |
| 29/09/2026 | Aviso "llegar 10 minutos antes" en confirmaciones y recordatorios (a la dueña le estresa la impuntualidad) |

## Lo que NO hace (por ahora)

Venta de productos, pagos en línea, facturación o DIAN, relojes y ropa, varios empleados, cuentas para clientes,
aplicación para instalar y ficha clínica (datos de salud sensibles).

## Diseño

- **Boceto aprobado:** `D:\Proyecto_nuevo\boceto\index.html` (se abre con doble clic). Tiene Inicio, Faciales,
  Corporales, detalle de servicio, Nosotros, Contacto y el panel completo (9 secciones, incluida una vista previa de
  la agenda de la fase 2). El usuario dijo que el boceto **puede cambiar**.
- **Logo:** captura de Instagram (circular). Recortes en `static/img/logo-simbolo.png` (figura, fondo transparente) y
  `static/img/logo-circulo.png` (logo completo). Falta el archivo original en buena calidad.
- **Colores del logo:** fucsia `#C749A7`, verde `#67B022`, azul `#5D7FCD`. Para que el texto se lea bien se usan tonos
  más oscuros: primario `#A83A8C`, primario oscuro `#5E1D4C`, verde `#3F7A12` / `#4F8F1C` / `#A6D96A` (sobre fondo
  oscuro), azul `#3F63B5`, fondo `#FFFAFC`, suave `#F8EAF3`, texto `#2A1F27`, texto secundario `#6B5A66`,
  borde `#EEDCE8`.
- **Panel (Unfold):** escala primaria en OKLCH con tono 339.3; el 600 es `#A83A8C` (ver `config/settings.py`).
- **Tipografías:** Cormorant Garamond (títulos), Jost (texto), Great Vibes ("Claudia" del logo de texto).
- **Menú:** Inicio · Faciales · Corporales · Nosotros · Contacto. En el celular, botón ☰. WhatsApp flotante siempre
  visible y sin nada que lo tape.

## Tecnología

| Parte | Tecnología |
|---|---|
| Páginas y lógica | Django 6.1 (plantillas renderizadas en el servidor, sin React ni Vue) |
| Panel de la dueña | Django Admin + django-unfold |
| Diseño | Tailwind CSS (compilado con Node 24) |
| Interacciones | Alpine.js; htmx opcional para la agenda de la fase 2 |
| Slider | Swiper |
| Fotos | Pillow (reducir y convertir a WebP) |
| Base de datos | MariaDB 12.3 con PyMySQL |
| Pruebas | pytest y Playwright |

## Etapas de construcción

| Etapa | Contenido | Estado |
|---|---|---|
| 1. La base | Django + MariaDB + panel en /panel/ | ✅ Lista (29/09/2026) |
| 2. Las tablas | Modelos de la fase 1, panel con sus secciones, traducir Unfold al español | Siguiente |
| 3. Datos de ejemplo | Los 8 servicios, el slider, la tecnología, las preguntas y el horario | |
| 4. El diseño | Tailwind, plantilla base, encabezado, pie y WhatsApp flotante | |
| 5. Las páginas | Inicio, Faciales, Corporales, detalle, Nosotros, Contacto, aviso de privacidad, 404 | |
| 6. Calidad | Fotos WebP, Google (SEO), pruebas en computador y celular | |
| 7. Prueba con la dueña | Ajustes y publicación | |
| Fase 2 | Agenda en línea | |

## Servicios de ejemplo (precios y duraciones inventados)

| Servicio | Categoría | Duración | Precio |
|---|---|---|---|
| Limpieza facial profunda (pasos reales de la dueña) | Facial | 75 a 90 min | $90.000 |
| Plasma rico en plaquetas | Facial | 45 a 60 min | $180.000 |
| Hidratación facial con máscara LED (inventado) | Facial | 40 a 50 min | $70.000 |
| Masaje relajante | Corporal | 50 a 60 min | $70.000 |
| Levantamiento de glúteos | Corporal | 45 a 60 min | Desde $80.000 por sesión |
| Depilación láser | Corporal | 15 a 45 min | Desde $50.000 |
| Combo limpieza facial + plasma | Facial (combo) | 2 h a 2 h 30 min | $240.000 (antes $270.000) |
| Paquete de depilación láser (5 sesiones) | Corporal (combo) | 15 a 45 min por sesión | Desde $220.000 |

Pasos reales de la limpieza facial profunda: limpieza con jabón facial, exfoliación, mascarilla para comedones,
vapor, extracción manual y con hidrafacial, mascarilla según el tipo de piel, aparatología para desinflamar,
hidratación con velo, máscara LED, masaje manual y bloqueador.

## Pendiente de la dueña o del usuario

- Lista real de servicios con precios y duraciones (una foto de la lista sirve).
- Número de WhatsApp, teléfono, enlace de Facebook, ciudad y si el spa aparece en Google Maps.
- Fotos del spa (local, procedimientos, antes y después con permiso escrito) para el slider y las páginas.
- Archivo original del logo (PNG con fondo transparente o SVG).
- **Permisos de salud** para anunciar el plasma rico en plaquetas y la depilación láser.
- Cuidados reales antes y después de cada servicio (los del boceto son de ejemplo).
- Si se usa Git para guardar el historial del código (el usuario todavía no respondió).
- Hosting y dominio: se cotizan antes de publicar.
