# Decisiones del proyecto Claudia Spa

Registro de lo decidido con el usuario (Jose Miguel, hijo de la dueña). Actualizado el 01/10/2026.

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
| 01/10/2026 | Git con un commit por etapa; repositorio público `josemartinez0821-design/Proyecto-clauspa`. Las respuestas de la entrevista a la dueña no se suben |
| 01/10/2026 | Detalle de servicio más completo (idea del usuario): descripción en párrafos, "Ideal para" y "Avísanos antes si…" (casos en que la persona debe avisar antes, como embarazo o alergias), además de los cuidados antes y después |
| 01/10/2026 | Las fotos se convierten a WebP y se reducen al subirlas (no en la etapa 6) |
| 01/10/2026 | Textos de Unfold traducidos con un catálogo propio (`locale/`), compilado con `manage.py compilar_traducciones` porque Windows no trae msgfmt |
| 01/10/2026 | Datos de ejemplo con `manage.py cargar_ejemplos` (solo con DEBUG=True); los textos están en `contenido/ejemplos.py` y las fotos se generan con los colores del logo y la marca "Foto de ejemplo" |
| 01/10/2026 | "Destacados" de Inicio = los 4 más pedidos según la dueña: limpieza facial, plasma, masaje relajante y levantamiento de glúteos (el combo sale en el slider) |
| 01/10/2026 | Las diapositivas llevan un texto pequeño opcional sobre el título ("Promoción del mes"), como en el boceto |
| 01/10/2026 | La dirección del spa no va en el repositorio público: se escribe en el panel |
| 01/10/2026 | Clientes sin registro ni cuentas: piden la cita por WhatsApp o llamada (fase 1) o con la agenda en línea solo con nombre y celular (fase 2) |
| 01/10/2026 | Tailwind CSS 4 (sí funciona con Smart App Control), Alpine.js y Swiper instalados con npm. El CSS compilado y las librerías se guardan en `static/` y se suben al repositorio: el servidor no necesita Node |
| 01/10/2026 | Letras desde Google Fonts por ahora; en la etapa 6 se decide si se sirven desde el propio sitio |
| 01/10/2026 | Mientras no haya número de WhatsApp, los botones abren WhatsApp con el mensaje y dejan elegir el chat |
| 01/10/2026 | Servicios con "la duración es por sesión" (paquetes y planes): se muestra "Aprox. 15 a 45 min por sesión" |
| 01/10/2026 | Nosotros muestra "años de experiencia" (campo opcional del panel) y "1 a 1, atención personalizada" |
| 01/10/2026 | El mapa de Contacto aparece solo cuando hay ciudad (sin ella, Google pondría el pin en otro barrio Canadá); "Cómo llegar" usa el enlace de Google Maps del panel o la dirección |
| 01/10/2026 | Aviso de privacidad con un texto base para la fase 1 (sin formularios); conviene que lo revise alguien que sepa de la Ley 1581 antes de publicar, y se actualiza en la fase 2 |
| 01/10/2026 | Fotos de referencia de Unsplash (licencia libre) mientras llegan las reales: viven fuera del repositorio (`D:\Proyecto_nuevo\fotos-ejemplo`, con `CREDITOS.md`) y se cargan con `cargar_ejemplos --fotos`. **Nunca** una foto de banco como si fuera la dueña; antes de publicar se cambian por fotos reales |
| 01/10/2026 | Cada foto se guarda también en 480, 960 y 1600 px (srcset); al cambiarla o borrarla se borran sus archivos. `manage.py generar_tamanos` completa las copias de fotos antiguas |
| 01/10/2026 | Letras servidas desde el propio sitio (Fontsource, OFL): sin Google Fonts, más rápido y sin enviar datos a Google |
| 01/10/2026 | SEO: título, descripción, dirección canónica y Open Graph por página; datos del negocio para Google (schema.org/DaySpa) en Inicio y Contacto; `sitemap.xml` y `robots.txt` |
| 01/10/2026 | Accesibilidad revisada con axe (WCAG 2.1 AA): sin errores en las 6 páginas, en computador y celular. El verde de WhatsApp se oscureció a `#1A7A43` para cumplir el contraste |

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
  borde `#EEDCE8`, botones de WhatsApp `#1A7A43`.
- **Panel (Unfold):** escala primaria en OKLCH con tono 339.3; el 600 es `#A83A8C` (ver `config/settings.py`).
- **Tipografías:** Cormorant Garamond (títulos), Jost (texto), Great Vibes ("Claudia" del logo de texto).
- **Menú:** Inicio · Faciales · Corporales · Nosotros · Contacto. En el celular, botón ☰. WhatsApp flotante siempre
  visible y sin nada que lo tape.

## Tecnología

| Parte | Tecnología |
|---|---|
| Páginas y lógica | Django 6.1 (plantillas renderizadas en el servidor, sin React ni Vue) |
| Panel de la dueña | Django Admin + django-unfold |
| Diseño | Tailwind CSS 4 (compilado con Node 24; fuente en `static/src/sitio.css`) |
| Interacciones | Alpine.js; htmx opcional para la agenda de la fase 2 |
| Slider | Swiper |
| Fotos | Pillow (reducir y convertir a WebP) |
| Base de datos | MariaDB 12.3 con PyMySQL |
| Pruebas | pytest y Playwright |

## Etapas de construcción

| Etapa | Contenido | Estado |
|---|---|---|
| 1. La base | Django + MariaDB + panel en /panel/ | ✅ Lista (29/09/2026) |
| 2. Las tablas | Modelos de la fase 1, panel con sus secciones, traducir Unfold al español | ✅ Lista (01/10/2026) |
| 3. Datos de ejemplo | Los 8 servicios con descripción y cuidados completos, el slider, la tecnología, las preguntas y el horario | ✅ Lista (01/10/2026) |
| 4. El diseño | Tailwind, plantilla base, encabezado, pie y WhatsApp flotante | ✅ Lista (01/10/2026) |
| 5. Las páginas | Inicio, Faciales, Corporales, detalle, Nosotros, Contacto, aviso de privacidad, 404 | ✅ Lista (01/10/2026) |
| 6. Calidad | Fotos en varios tamaños, letras desde el propio sitio, Google (SEO), accesibilidad, pruebas en computador y celular | ✅ Lista (01/10/2026) |
| 7. Prueba con la dueña | Cuenta de la dueña, datos y fotos reales, ajustes, hosting, dominio y publicación (con PageSpeed real) | Siguiente |
| Fase 2 | Agenda en línea | |

## Servicios de ejemplo (precios y duraciones inventados)

Los textos completos de cada uno (descripción, ideal para, qué incluye, cuidados, "avísanos antes si…" y
recomendaciones) están en `contenido/ejemplos.py`. Los que van en Inicio: limpieza facial, plasma, masaje y glúteos.

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
- Fotos del spa (local, procedimientos, antes y después con permiso escrito) para el slider y las páginas, y una foto
  de la dueña para Nosotros. Las de referencia de Unsplash se reemplazan antes de publicar.
- Archivo original del logo (PNG con fondo transparente o SVG).
- **Permisos de salud** para anunciar el plasma rico en plaquetas y la depilación láser.
- Cuidados reales antes y después de cada servicio, y los casos de "Avísanos antes si…" (los de ejemplo los escribe
  Claude; la dueña debe revisarlos, sobre todo los del plasma y el láser).
- Hosting y dominio: se cotizan antes de publicar.
