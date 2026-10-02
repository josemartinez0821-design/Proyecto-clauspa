"""
Configuración de Django para Claudia Spa.

Los valores secretos o que cambian entre el PC y el servidor (base de datos,
clave secreta, modo de desarrollo) se leen del archivo .env, que no se sube a GitHub.
"""

from pathlib import Path

import environ
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")


# Aplicaciones

INSTALLED_APPS = [
    # Unfold va antes del admin de Django: le cambia el diseño al panel.
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps del proyecto
    "servicios",
    "contenido",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "contenido.contexto.sitio",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Base de datos: MariaDB

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        "TEST": {
            "NAME": "test_claudia_spa",
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_ci",
        },
    }
}


# Contraseñas

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Idioma y hora: Colombia

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# Traducciones propias: los textos de Unfold que Django no trae en español.
# Después de editar el .po: python manage.py compilar_traducciones
LOCALE_PATHS = [BASE_DIR / "locale"]


# Archivos estáticos (CSS, JavaScript, imágenes del diseño) y fotos que sube la dueña

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# Correo: en desarrollo los correos se muestran en la consola en lugar de enviarse.

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}


# Panel de la dueña (Unfold). Los colores salen del fucsia del logo:
# el tono 600 es #A83A8C, el mismo de los botones de la página.

UNFOLD = {
    "SITE_TITLE": "Claudia Spa",
    "SITE_HEADER": "Claudia Spa",
    "SITE_SUBHEADER": "Relajación y belleza",
    "SITE_SYMBOL": "spa",
    "SHOW_HISTORY": False,
    "DASHBOARD_CALLBACK": "config.panel.inicio",
    # Menú lateral: las secciones del boceto, en el mismo orden.
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Mi página",
                "items": [
                    {"title": "Inicio", "icon": "home", "link": reverse_lazy("admin:index")},
                    {
                        "title": "Servicios",
                        "icon": "spa",
                        "link": reverse_lazy("admin:servicios_servicio_changelist"),
                    },
                    {
                        "title": "Slider",
                        "icon": "view_carousel",
                        "link": reverse_lazy("admin:contenido_diapositiva_changelist"),
                    },
                    {
                        "title": "Tecnología",
                        "icon": "auto_awesome",
                        "link": reverse_lazy("admin:contenido_tecnologia_changelist"),
                    },
                    {
                        "title": "Preguntas frecuentes",
                        "icon": "help",
                        "link": reverse_lazy("admin:contenido_preguntafrecuente_changelist"),
                    },
                    {
                        "title": "Nosotros",
                        "icon": "favorite",
                        "link": reverse_lazy("admin:contenido_nosotros_changelist"),
                    },
                    {
                        "title": "Datos del negocio",
                        "icon": "storefront",
                        "link": reverse_lazy("admin:contenido_negocio_changelist"),
                    },
                ],
            },
            {
                "title": "Mi cuenta",
                "separator": True,
                "items": [
                    {
                        "title": "Cambiar mi contraseña",
                        "icon": "lock",
                        "link": reverse_lazy("admin:password_change"),
                    },
                    {
                        "title": "Usuarios",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": "config.panel.solo_administrador",
                    },
                ],
            },
        ],
    },
    "COLORS": {
        "primary": {
            "50": "oklch(97.6% 0.018 339.3)",
            "100": "oklch(94.8% 0.036 339.3)",
            "200": "oklch(90.2% 0.068 339.3)",
            "300": "oklch(83.0% 0.110 339.3)",
            "400": "oklch(72.5% 0.160 339.3)",
            "500": "oklch(63.5% 0.175 339.3)",
            "600": "oklch(53.2% 0.171 339.3)",
            "700": "oklch(46.5% 0.140 339.3)",
            "800": "oklch(40.0% 0.120 339.3)",
            "900": "oklch(34.5% 0.100 339.3)",
            "950": "oklch(25.5% 0.075 339.3)",
        },
    },
}
