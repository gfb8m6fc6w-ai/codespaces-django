"""
إعدادات المشروع المحسّنة
توفر كل إعدادات التطبيق في مكان واحد
"""

import os
from pathlib import Path
from typing import List
import logging

# إعداد السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==========================================
# المسارات الأساسية
# ==========================================

PROJECT_ROOT = Path(__file__).parent.absolute()
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR = PROJECT_ROOT / ".billiards_data"
LOGS_DIR = PROJECT_ROOT / "logs"

# إنشاء المجلدات الضرورية
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

logger.info(f"✅ المسارات الأساسية جاهزة")

# ==========================================
# إعدادات التطبيق
# ==========================================

APP_NAME = "5A Diamond System Pro"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "نظام احترافي لتحليل تسديدات البلياردو بنظام الدايمند العشري"
APP_AUTHOR = "5A System Pro"
APP_EMAIL = "info@5asystempro.com"

# ==========================================
# إعدادات الخادم
# ==========================================

SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 8001))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
RELOAD = os.getenv("RELOAD", "False").lower() == "true"

logger.info(f"🔧 إعدادات الخادم: {SERVER_HOST}:{SERVER_PORT}")

# ==========================================
# إعدادات قاعدة البيانات
# ==========================================

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/billiards.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", "False").lower() == "true"

# ==========================================
# إعدادات السجلات
# ==========================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / "app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

logger.info(f"📝 ملف السجل: {LOG_FILE}")

# ==========================================
# إعدادات CORS
# ==========================================

ALLOWED_ORIGINS: List[str] = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
]

if os.getenv("ALLOWED_ORIGINS"):
    ALLOWED_ORIGINS.extend(os.getenv("ALLOWED_ORIGINS").split(","))

# ==========================================
# إعدادات الأمان
# ==========================================

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    logger.warning("⚠️ SECRET_KEY غير محدد! يجب تعيينه في متغيرات البيئة")
    SECRET_KEY = "dev-secret-key-change-in-production"

CSRF_ENABLED = os.getenv("CSRF_ENABLED", "True").lower() == "true"
CORS_ENABLED = os.getenv("CORS_ENABLED", "True").lower() == "true"

# ==========================================
# إعدادات التخزين
# ==========================================

STORAGE_TYPE = os.getenv("STORAGE_TYPE", "json")  # json, sqlite, mongodb
SHOTS_FILE = DATA_DIR / "shots.json"
STATISTICS_FILE = DATA_DIR / "statistics.json"

# ==========================================
# إعدادات الاختبارات
# ==========================================

TEST_DATABASE_URL = f"sqlite:///{DATA_DIR}/test.db"
TEST_DEBUG = True

# ==========================================
# إعدادات الأداء
# ==========================================

CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
CACHE_TTL = int(os.getenv("CACHE_TTL", 300))  # 5 دقائق
MAX_SHOTS = int(os.getenv("MAX_SHOTS", 10000))

# ==========================================
# إعدادات التصدير والاستيراد
# ==========================================

IMPORT_EXPORT_DIR = DATA_DIR / "import_export"
IMPORT_EXPORT_DIR.mkdir(exist_ok=True)
MAX_IMPORT_SIZE = 50 * 1024 * 1024  # 50 MB

# ==========================================
# إعدادات Django (إذا كانت مستخدمة)
# ==========================================

DJANGO_DEBUG = DEBUG
DJANGO_ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
DJANGO_SECRET_KEY = SECRET_KEY

# ==========================================
# إعدادات البيئة
# ==========================================

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, staging, production

if ENVIRONMENT == "production":
    DEBUG = False
    CACHE_ENABLED = True
    logger.info("🚀 التطبيق في وضع الإنتاج")
else:
    logger.info("🔧 التطبيق في وضع التطوير")

# ==========================================
# التحقق من الإعدادات الحرجة
# ==========================================

def verify_settings():
    """التحقق من الإعدادات الحرجة"""
    if ENVIRONMENT == "production":
        if not SECRET_KEY or SECRET_KEY == "dev-secret-key-change-in-production":
            raise ValueError("❌ يجب تعيين SECRET_KEY آمن في الإنتاج")
        
        if DEBUG:
            raise ValueError("❌ لا يمكن تشغيل DEBUG في الإنتاج")
    
    logger.info("✅ تم التحقق من الإعدادات بنجاح")

# التحقق عند الاستيراد
verify_settings()

logger.info(f"✅ تم تحميل الإعدادات للبيئة: {ENVIRONMENT}")
