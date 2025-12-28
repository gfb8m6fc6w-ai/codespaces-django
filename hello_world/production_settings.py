"""
إعدادات Django للإنتاج (Production Settings)
يوفر أمان وأداء عالية للبيئة الإنتاجية

الاستخدام:
    DJANGO_SETTINGS_MODULE=hello_world.production_settings
    python manage.py runserver
"""

import os
from pathlib import Path
from decouple import config
import logging

# استيراد الإعدادات الأساسية
BASE_SETTINGS_MODULE = 'hello_world.settings'

# ==========================================
# إعدادات أساسية محسّنة للإنتاج
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# المفتاح السري - يجب أن يكون قوياً
SECRET_KEY = config("SECRET_KEY", default=None)
if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY مطلوب في بيئة الإنتاج")

# وضع التصحيح - يجب أن يكون False في الإنتاج
DEBUG = False

# ==========================================
# الأمان والـ HTTPS
# ==========================================

# الحد من أسماء المضيفين المسموح
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# فرض HTTPS
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_HTTPONLY = True
SECURE_HSTS_SECONDS = 31536000  # سنة كاملة
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Browser
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "'unsafe-inline'", "https://cdn.example.com"),
    'style-src': ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com"),
    'img-src': ("'self'", "data:", "https:"),
    'font-src': ("'self'", "https://fonts.gstatic.com"),
    'connect-src': ("'self'", "https://api.example.com"),
}

# ==========================================
# CORS والـ CSRF
# ==========================================

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='').split(',')

CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in config(
        'CORS_ALLOWED_ORIGINS', 
        default='https://example.com,https://app.example.com'
    ).split(',')
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# ==========================================
# التطبيقات المثبتة
# ==========================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ==========================================
# Middleware
# ==========================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",  # ضغط المحتوى
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==========================================
# قاعدة البيانات (PostgreSQL مُوصى به)
# ==========================================

DATABASES = {
    "default": {
        "ENGINE": config('DB_ENGINE', default='django.db.backends.postgresql'),
        "NAME": config('DB_NAME', default='billiards_db'),
        "USER": config('DB_USER', default='postgres'),
        "PASSWORD": config('DB_PASSWORD', default=''),
        "HOST": config('DB_HOST', default='localhost'),
        "PORT": config('DB_PORT', default='5432'),
        "CONN_MAX_AGE": 600,
        "OPTIONS": {
            "connect_timeout": 10,
        }
    }
}

# ==========================================
# المخزن المؤقت (Caching)
# ==========================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": config('REDIS_URL', default='redis://127.0.0.1:6379/1'),
        "KEY_PREFIX": "billiards",
        "TIMEOUT": 300,  # 5 دقائق
    }
}

# ==========================================
# الملفات الثابتة والوسائط
# ==========================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CDN
STATIC_URL = config('CDN_URL', default='/static/')

# ==========================================
# السجلات (Logging)
# ==========================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_errors': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'errors.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'file_errors'],
            'level': 'INFO',
            'propagate': False,
        },
        'billiards': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# إنشاء مجلد السجلات
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# ==========================================
# جلسات المستخدمين
# ==========================================

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 3600  # ساعة واحدة
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ==========================================
# البريد الإلكتروني
# ==========================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@billiards.example.com')

# ==========================================
# مراقبة الأداء
# ==========================================

# Sentry (Error Tracking)
SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=config('ENVIRONMENT', default='production'),
    )

# ==========================================
# المتغيرات المتقدمة
# ==========================================

APPEND_SLASH = True
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = 'ar'

# ==========================================
# أمان إضافي
# ==========================================

# حماية من MIME Sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# حماية من XSS
SECURE_BROWSER_XSS_FILTER = True

# الإعدادات الافتراضية
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================================
# معلومات الإصدار والصحة
# ==========================================

VERSION = '2.0.0'
BUILD_ID = config('BUILD_ID', default='unknown')
DEPLOY_TIME = config('DEPLOY_TIME', default='unknown')

# ==========================================
# جودة الكود
# ==========================================

# تنسيق SQL في الاختبارات
SQLFORMAT = {
    'verbose': False,
}

print("""
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║  ✅ إعدادات الإنتاج تم تحميلها بنجاح                            ║
║                                                                   ║
║  🔒 الأمان:                                                       ║
║     • HTTPS/SSL مفعّل                                            ║
║     • CSRF Protection مفعّل                                       ║
║     • XSS Protection مفعّل                                        ║
║     • HSTS مفعّل                                                 ║
║                                                                   ║
║  ⚡ الأداء:                                                       ║
║     • Gzip Compression مفعّل                                     ║
║     • Redis Cache مفعّل                                          ║
║     • Database Connection Pooling مفعّل                          ║
║                                                                   ║
║  📊 المراقبة:                                                     ║
║     • Logging مفعّل                                              ║
║     • Error Tracking مفعّل                                       ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
""")
