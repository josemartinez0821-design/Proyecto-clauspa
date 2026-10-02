# Modelo de datos de Claudia Spa

Base MariaDB `claudia_spa` (utf8mb4). Las tablas las crean las **migraciones de Django** a partir de los modelos;
no se escriben a mano. Actualizado el 29/09/2026.

Son **13 tablas**: 9 de la fase 1 (sitio y panel) y 4 de la fase 2 (agenda en línea). Django agrega sus tablas
propias (usuarios, permisos, sesiones, historial del panel).

## Fase 1: sitio y panel

### `negocio` (una sola fila)
nombre, lema ("Relajación y belleza"), logo, whatsapp, telefono, direccion, barrio, ciudad, enlace_mapa,
saludo_whatsapp, instagram, facebook, tiktok, enlace_resenas, titulo_nosotros, texto_nosotros, foto_duena,
actualizado.

### `horario_atencion`
dia_semana (1 = lunes … 7 = domingo), hora_apertura, hora_cierre.
Un día puede tener dos franjas (9–13 y 14–19). Un día sin filas está cerrado. Sirve para mostrar el horario (fase 1)
y para calcular la agenda (fase 2).

### `servicio`
nombre, slug (dirección web, único), categoria (facial o corporal), es_combo, descripcion_breve, descripcion,
que_incluye (un paso por línea), **cuidados_antes** (uno por línea), **cuidados_despues** (uno por línea),
recomendaciones, duracion_min y duracion_max (minutos), precio (pesos enteros), tipo_precio (fijo o "desde"),
precio_anterior (opcional, para mostrar el ahorro), sufijo_precio (opcional, por ejemplo "por sesión"),
destacado, visible, orden, requiere_abono (fase 2), se_pide_en_linea (fase 2), creado, actualizado.

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
imagen, texto_alternativo, orden.

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

- Precios en pesos enteros, sin centavos.
- `duracion_max` nunca menor que `duracion_min`.
- `precio_anterior`, si existe, mayor que `precio`.
- Celular de cliente único.
- Un servicio con citas **no se puede borrar**: se oculta (FK protegida), para no perder el historial.
- Máximo 4 diapositivas activas y mínimo 1 (validado en el panel).
- En la agenda, una cita ocupa la duración máxima del servicio más la preparación; las reservas simultáneas de la
  misma hora se resuelven con una transacción que bloquea las filas del día (MariaDB no tiene restricciones de
  exclusión).
