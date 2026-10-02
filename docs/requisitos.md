# Requisitos de Claudia Spa

Qué hace el sistema, punto por punto. Actualizado el 29/09/2026.

- **S** = sitio público (funcional)
- **P** = panel de la dueña (funcional)
- **C** = citas en línea, fase 2 (funcional)
- **Q** = calidad (no funcional)

## 1. Sitio público (fase 1)

Cada opción del menú es su propia página: `/`, `/faciales/`, `/corporales/`, `/nosotros/`, `/contacto/` y el
detalle de cada servicio (por ejemplo `/faciales/limpieza-facial-profunda/`).

| Código | Requisito | Detalle |
|---|---|---|
| S-01 | Menú | Inicio · Faciales · Corporales · Nosotros · Contacto. En el computador, barra con el logo; en el celular, logo y botón ☰ |
| S-02 | Slider de Inicio | De 1 a 4 diapositivas con imagen, título, texto corto y un botón. Avanza sola cada 6 s con transición suave; se pausa al pasar el mouse o al tocarla; flechas y puntos (en el celular solo puntos y deslizar con el dedo). Con una sola diapositiva no se mueve. Texto sobre una capa oscura suave |
| S-03 | Resto de Inicio | Servicios destacados, sección de tecnología, resumen de Nosotros con enlace a su página y franja con dirección, horario y enlace a Contacto |
| S-04 | Lista de servicios | Una página por categoría con tarjetas: foto, nombre, descripción breve, duración aproximada y precio. Solo los visibles, en el orden que defina la dueña. Los combos llevan la etiqueta "Combo" y el precio anterior tachado |
| S-05 | Detalle del servicio | Fotos, descripción, precio, duración aproximada y desplegables: **Qué incluye**, **Antes de tu cita**, **Después de tu cita** (con la nota "Además, te damos indicaciones personalizadas según tu tipo de piel") y Recomendaciones |
| S-06 | "También te puede interesar" | Hasta 3 servicios de la misma categoría al final del detalle |
| S-07 | Precios | En pesos colombianos, fijos ("$80.000") o "desde" ("Desde $80.000"), con sufijo opcional ("por sesión") |
| S-08 | Duraciones | Siempre aproximadas ("Aprox. 45 a 60 min"; desde 2 h se muestran en horas), con la nota "Los tiempos pueden variar según cada persona" |
| S-09 | Botón WhatsApp | Abre el chat del spa con el mensaje "Hola, vi la página de Claudia Spa y quiero pedir una cita para <servicio>." |
| S-10 | Botón Llamar | En el celular marca directo; en el computador muestra el número |
| S-11 | WhatsApp flotante | En todas las páginas, con saludo; ningún elemento lo tapa |
| S-12 | Nosotros | Historia, quién es la dueña (foto y texto breve con su experiencia), fotos del local y enlace a reseñas de Google. **Sin fotos de diplomas** |
| S-13 | Contacto | Dirección, mapa, botón "Cómo llegar" (Google Maps), horario por días, WhatsApp, teléfono, redes y preguntas frecuentes desplegables. Aviso de que también se atiende a domicilio (por WhatsApp) |
| S-14 | Pie de página | Logo en círculo, dirección, horario, contacto, redes y enlace al aviso de privacidad |
| S-15 | Aviso de privacidad | Página sencilla que explica qué datos se usan y para qué |
| S-16 | Página no encontrada | Mensaje amable y botón para volver al inicio |

## 2. Panel de la dueña (fase 1) — en /panel/

| Código | Requisito | Detalle |
|---|---|---|
| P-01 | Iniciar sesión | Con correo o usuario y contraseña; botón para cerrar sesión |
| P-02 | Recuperar la contraseña | El enlace llega al correo del hijo (ella no usa Gmail) |
| P-03 | Cambiar la contraseña | Desde "Mi cuenta" |
| P-04 | Servicios | Crear, editar, ocultar, ordenar y destacar. Campos: nombre, categoría, es combo, descripción breve y completa, qué incluye, **cuidados antes**, **cuidados después**, recomendaciones, duración mínima y máxima, precio, tipo de precio, precio anterior, sufijo, fotos |
| P-05 | Slider | Crear, editar, ordenar, activar o desactivar diapositivas: mínimo 1 y **máximo 4 activas**. Fechas opcionales de inicio y fin para que una promoción aparezca y se quite sola |
| P-06 | Nosotros | Título, texto, foto de la dueña y fotos del local |
| P-07 | Preguntas frecuentes | Crear, editar, ordenar y ocultar |
| P-08 | Datos del negocio | Nombre, lema, logo, dirección, barrio, ciudad, enlace del mapa, WhatsApp, teléfono, saludo del WhatsApp, redes, enlace a reseñas y horario por día (una o dos franjas, o cerrado) |
| P-09 | Fotos | Se reducen y se convierten a WebP solas al subirlas. JPG, PNG o WebP de hasta 10 MB |
| P-10 | Cambios al instante | Lo que ella guarda se ve en la página de inmediato |
| P-11 | Tecnología | Crear, editar, ordenar y ocultar los equipos que se muestran en Inicio |

El panel tiene además una página de inicio con resumen (servicios visibles, diapositivas activas, preguntas) y
accesos rápidos, y un enlace "Ver mi página".

## 3. Citas en línea (fase 2)

### Reglas (salen de la entrevista a la dueña; se cambian desde el panel)

| Regla | Valor |
|---|---|
| Días de atención | Lunes a sábado |
| Horario | 9:00 a. m. a 1:00 p. m. y 2:00 p. m. a 7:00 p. m. |
| Preparación entre citas | 15 minutos |
| Anticipación mínima | 1 día (desde el día siguiente) |
| Anticipación máxima | 30 días |
| Horas de inicio | Cada 30 minutos |
| Quién confirma | La dueña, normalmente en menos de 2 horas |
| Plazo para confirmar | 3 horas dentro de su horario de atención |
| Cancelaciones | En cualquier momento |
| Datos del cliente | Nombre y celular |
| Aviso de solicitudes | Por WhatsApp (el mensaje del cliente es el aviso) |
| Abono | Por transferencia, en los servicios que ella marque |
| Domicilios | No entran en la agenda en línea; se acuerdan por WhatsApp y ella los agrega a mano |

### Requisitos

| Código | Requisito | Detalle |
|---|---|---|
| C-01 | Página "Pedir cita" | Servicio → día → hora libre → nombre y celular → aceptar el aviso de privacidad → "Confirmar por WhatsApp" |
| C-02 | Días disponibles | Lunes a sábado, desde el día siguiente hasta 30 días adelante, sin días bloqueados |
| C-03 | Horas libres | Cada cita ocupa la **duración máxima** del servicio más 15 min; debe terminar antes del almuerzo o del cierre; no se cruza con citas, solicitudes pendientes ni bloqueos |
| C-04 | Solicitud pendiente | Lleva un número (por ejemplo #0012); mientras está pendiente, esa hora aparece ocupada |
| C-05 | Confirmación por WhatsApp | Mensaje ya escrito para el spa con servicio, día, hora, nombre y número de solicitud |
| C-06 | Plazo para confirmar | Si la dueña no confirma a tiempo, la solicitud vence y la hora se libera. Nunca se ofrece una hora que empiece antes de que venza el plazo |
| C-07 | Límites | Una sola solicitud pendiente por celular; máximo 3 solicitudes por hora desde el mismo dispositivo |
| C-08 | Trampa para robots | Campo oculto; si llega basura, verificador gratuito (por ejemplo Cloudflare Turnstile) |
| C-09 | Números bloqueados | No pueden enviar solicitudes; ven un mensaje amable para escribir por WhatsApp |
| C-10 | Panel — Solicitudes | Pendientes con el tiempo que les queda; confirmar o rechazar con un toque; al confirmar, WhatsApp con el mensaje de confirmación (pide llegar 10 min antes e incluye datos del abono si aplica) |
| C-11 | Panel — Agenda | Por día y por semana, en celular y computador; ver, mover y cancelar citas |
| C-12 | Panel — Citas a mano | Las que llegan por WhatsApp, llamada, Facebook o en persona; opción a domicilio con dirección y tiempo de desplazamiento |
| C-13 | Panel — Bloqueos | Bloquear horas o días completos |
| C-14 | Panel — Reglas | Cambiar el horario por día y las reglas de la tabla anterior |
| C-15 | Panel — Citas de mañana | Botón de recordatorio por WhatsApp (pide llegar 10 min antes; puede incluir los cuidados "antes" del servicio) |
| C-16 | Estados de la cita | Pendiente, confirmada, atendida, cancelada, no asistió y vencida; marca "llegó tarde" |
| C-17 | Abono | Servicio "requiere abono"; en la cita, "abono recibido". El sistema no cobra |
| C-18 | Panel — Clientes | Lista por celular con historial (citas, inasistencias, llegadas tarde), notas y bloqueo |
| C-19 | Panel — Resumen | Solicitudes pendientes, citas de la semana, servicios más pedidos |

## 4. Calidad

| Código | Requisito | Detalle |
|---|---|---|
| Q-01 | Responsive | Desde celulares de 360 px hasta computadores grandes |
| Q-02 | Rápida | Inicio con 90 o más en PageSpeed Insights (celular); fotos WebP en varios tamaños; diapositivas 2 a 4 cargan después |
| Q-03 | Accesible | Contraste AA de WCAG, textos alternativos, uso con teclado, slider con pausa, respeto por "reducir movimiento" |
| Q-04 | Encontrable en Google | Título y descripción por página, direcciones legibles, datos de negocio local, sitemap |
| Q-05 | Segura | HTTPS, contraseñas cifradas, bloqueo temporal tras intentos fallidos, validación de todo lo que se envía o se sube |
| Q-06 | Copias de seguridad | Diarias de la base de datos y de las fotos, con prueba de restauración |
| Q-07 | Navegadores | Chrome, Safari, Edge y Firefox recientes, en Android, iPhone y Windows |
| Q-08 | Fácil para la dueña | Maneja el panel sola tras una explicación de 30 minutos o menos |
| Q-09 | Mantenible | Código ordenado, con control de versiones y esta documentación |
| Q-10 | Datos personales (fase 2) | Autorización obligatoria (Ley 1581 de 2012); solo nombre y celular; se borran si el cliente lo pide |
| Q-11 | Hora de Colombia | Todas las fechas y horas en America/Bogota |
| Q-12 | Sin choques (fase 2) | Si dos personas piden la misma hora a la vez, solo una la obtiene |
