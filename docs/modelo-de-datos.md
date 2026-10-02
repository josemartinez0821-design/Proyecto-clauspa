# Modelo de datos de Claudia Spa

Base MariaDB `claudia_spa` (utf8mb4). Las tablas las crean las **migraciones de Django** a partir de los modelos;
no se escriben a mano. Actualizado el 01/10/2026.

Los modelos de la fase 1 están en dos apps: `servicios` (servicio y foto_servicio) y `contenido` (todo lo demás).
Cada modelo fija el nombre de su tabla con `db_table`, así que las tablas se llaman como aparecen aquí.

Son **13 tablas**: 9 de la fase 1 (sitio y panel) y 4 de la fase 2 (agenda en línea). Django agrega sus tablas
propias (usuarios, permisos, sesiones, historial del panel).

## Fase 1: sitio y panel

### `negocio` (una sola fila)
nombre, lema ("Relajación y belleza"), logo, whatsapp, telefono, direccion, barrio, ciudad, enlace_mapa,
saludo_whatsapp, instagram, facebook, tiktok, enlace_resenas, titulo_nosotros, texto_nosotros, foto_duena,
actualizado.
Siempre tiene id 1 (`Negocio.cargar()`). WhatsApp y teléfono se guardan solo con los 10 dígitos (se aceptan con
espacios, guiones o +57). La sección **Nosotros** del panel edita esta misma fila (modelo proxy `Nosotros`, sin tabla
propia).

### `horario_atencion`
negocio (FK → negocio), dia_semana (1 = lunes … 7 = domingo), hora_apertura, hora_cierre.
Un día puede tener dos franjas (9–13 y 14–19). Un día sin filas está cerrado. Sirve para mostrar el horario (fase 1)
y para calcular la agenda (fase 2). La FK a negocio permite editar el horario dentro de "Datos del negocio".

### `servicio`
nombre (único), slug (dirección web, único), categoria (facial o corporal), es_combo, descripcion_breve,
descripcion, **ideal_para** (uno por línea), que_incluye (un paso por línea), recomendaciones (frecuencia, sesiones),
**cuidados_antes** (uno por línea), **cuidados_despues** (uno por línea), **consultar_antes** ("Avísanos antes si…",
uno por línea), duracion_min y duracion_max (minutos), precio (pesos enteros), tipo_precio (fijo o "desde"),
precio_anterior (opcional, para mostrar el ahorro), sufijo_precio (opcional, por ejemplo "por sesión"),
destacado, visible, orden, creado, actualizado.
`requiere_abono` y `se_pide_en_linea` se agregan en la fase 2, con su migración.

### `foto_servicio`
servicio (FK → servicio, se borra con él), imagen, texto_alternativo, orden.

### `diapositiva`
imagen, titulo, texto, texto_boton, destino (servicio, faciales, corporales, whatsapp, contacto o tecnología),
servicio (FK opcional → servicio; si el servicio se borra, queda vacío), activa, orden, fecha_inicio y fecha_fin
(opcionales).

### `tecnologia`
nombre, descripcion, foto, visible, orden.

### `pregunta_frecuente`
pregunta, respuesta, visible, orden.

### `foto_local`
negocio (FK → negocio, para editarlas dentro de Nosotros), imagen, texto_alternativo, orden.

Todas las fotos se aceptan en JPG, PNG o WebP de hasta 10 MB y se guardan reducidas y en WebP
(`contenido/imagenes.py`): slider 2400 px, fotos de servicios y del local 1600 px, tecnología y foto de la dueña
1200 px, logo 800 px.

### `usuario`
El usuario de Django (`auth_user`): usuario, correo, contraseña cifrada.

## Fase 2: agenda en línea

### `regla_agenda` (una sola fila)
anticipacion_min_dias (1), anticipacion_max_dias (30), intervalo_min (30), preparacion_min (15),
horas_confirmar (3), solicitudes_por_hora (3).

### `cliente`
nombre, celular (único), notas, bloqueado, autorizo_datos (fecha y hora), creado.

### `cita`
numero (único, por ejemplo 12 → "#0012"), cliente (FK), servicio (FK, protegido), inicio, fin (ya incluye la
preparación), estado (pendiente, confirmada, atendida, cancelada, no_asistio o vencida), origen (pagina, whatsapp,
llamada, facebook o en_persona), a_domicilio, direccion_domicilio, desplazamiento_min, llego_tarde,
abono_requerido, abono_recibido, vence (para las pendientes), notas, creado. Índice por (inicio, fin) para buscar
cruces rápido.

### `bloqueo`
inicio, fin, motivo.

## Relaciones

```text
servicio  1 ──── *  foto_servicio
servicio  1 ──── *  cita  * ──── 1  cliente
servicio  1 ──── *  diapositiva     (cuando el botón lleva a un servicio)
negocio y regla_agenda: una sola fila cada una
```

## Reglas que debe cuidar el sistema

- Precios en pesos enteros, sin centavos. En el panel se pueden escribir con puntos ("90.000").
- `duracion_max` nunca menor que `duracion_min` (también como restricción CHECK en la base).
- `precio_anterior`, si existe, mayor que `precio` (también como CHECK).
- En el horario, el cierre después de la apertura (CHECK) y sin franjas que se crucen el mismo día (panel).
- En las diapositivas, la fecha final no anterior a la inicial (CHECK); si el botón lleva a un servicio, hay que
  elegirlo.
- Celular de cliente único.
- Un servicio con citas **no se puede borrar**: se oculta (FK protegida), para no perder el historial.
- Máximo 4 diapositivas activas y mínimo 1 (validado en el panel: no se puede desactivar ni borrar la última
  activa).
- En la agenda, una cita ocupa la duración máxima del servicio más la preparación; las reservas simultáneas de la
  misma hora se resuelven con una transacción que bloquea las filas del día (MariaDB no tiene restricciones de
  exclusión).
