# Claudia Spa

Página web informativa y responsive para **Claudia Spa** ("Relajación y belleza"): muestra los servicios faciales y
corporales con precios y duraciones aproximadas, y las citas se piden por WhatsApp o por teléfono. Tiene un panel en
`/panel/` para que la dueña maneje servicios, slider, textos y fotos. La agenda en línea es la fase 2.

## Tecnología

Django 6.1 · Python 3.13 · MariaDB 12.3 (con PyMySQL) · django-unfold (panel) · Pillow ·
Tailwind CSS, Alpine.js y Swiper (en el sitio público).

## Cómo correrlo en el PC

1. Crear el entorno e instalar las dependencias:

   ```bash
   python -m venv .venv
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. Crear la base de datos `claudia_spa` (utf8mb4) y su usuario en MariaDB.
3. Copiar `.env.ejemplo` como `.env` y completar los valores.
4. Crear las tablas y el usuario administrador:

   ```bash
   .venv\Scripts\python.exe manage.py migrate
   .venv\Scripts\python.exe manage.py createsuperuser
   ```

5. (Opcional) Cargar los datos de ejemplo: 8 servicios, slider, tecnología, preguntas, horario y fotos de ejemplo.
   Solo funciona con `DEBUG=True` y se puede repetir sin duplicar nada:

   ```bash
   .venv\Scripts\python.exe manage.py cargar_ejemplos
   ```

6. Encender el servidor y abrir <http://127.0.0.1:8000/panel/>:

   ```bash
   .venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
   ```

Se usa PyMySQL en lugar de mysqlclient porque no necesita partes compiladas (ver `config/__init__.py`).

## Estilos del sitio (Tailwind CSS)

El CSS compilado (`static/css/sitio.css`) y las librerías (`static/vendor/`) ya vienen en el repositorio, así que
para correr el sitio no hace falta Node. Solo se necesita para cambiar el diseño:

```bash
npm install
npm run css:vigilar
```

`css:vigilar` recompila mientras se editan las plantillas. Antes de un commit: `npm run construir` (copia Alpine.js y
Swiper a `static/vendor/` y genera el CSS minificado).

## Documentación

En `docs/`: decisiones del proyecto, requisitos y modelo de datos.
