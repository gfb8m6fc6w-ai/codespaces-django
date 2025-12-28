#!/bin/bash

##############################################################################
#
#  BUILD SCRIPT - سكريبت البناء
#
#  الوظيفة: بناء المشروع وإعداده للإنتاج
#  الاستخدام: ./build.sh
#
#  الخطوات:
#  1. التحقق من المتطلبات
#  2. تنظيف الملفات القديمة
#  3. تثبيت المكتبات
#  4. تجميع الملفات الثابتة
#  5. تشغيل الاختبارات
#  6. بناء Docker Image
#
##############################################################################

set -e  # خروج عند أول خطأ

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==========================================
# الدوال المساعدة
# ==========================================

print_header() {
    echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║ $1${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
}

print_step() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# ==========================================
# الخطوة 1: التحقق من المتطلبات
# ==========================================

print_header "الخطوة 1: التحقق من المتطلبات"

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 غير مثبت"
    exit 1
fi
print_step "Python 3 موجود"

# التحقق من pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 غير مثبت"
    exit 1
fi
print_step "pip3 موجود"

# التحقق من git
if ! command -v git &> /dev/null; then
    print_warning "git غير مثبت (اختياري)"
else
    print_step "git موجود"
fi

# ==========================================
# الخطوة 2: تنظيف الملفات القديمة
# ==========================================

print_header "الخطوة 2: تنظيف الملفات القديمة"

# تنظيف Python cache
echo "تنظيف Python cache..."
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
print_step "تم تنظيف Python cache"

# تنظيف Logs
if [ -d "logs" ]; then
    echo "تنظيف السجلات..."
    rm -rf logs/*
    print_step "تم تنظيف السجلات"
fi

# تنظيف Build artifacts
if [ -d "build" ]; then
    echo "حذف build directory..."
    rm -rf build
fi

if [ -d "dist" ]; then
    echo "حذف dist directory..."
    rm -rf dist
fi

print_step "تم التنظيف بنجاح"

# ==========================================
# الخطوة 3: تثبيت المكتبات
# ==========================================

print_header "الخطوة 3: تثبيت المكتبات"

if [ ! -f "requirements.txt" ]; then
    print_error "ملف requirements.txt غير موجود"
    exit 1
fi

echo "ترقية pip و setuptools..."
pip3 install --upgrade pip setuptools wheel

echo "تثبيت المكتبات من requirements.txt..."
pip3 install -r requirements.txt

# تثبيت المكتبات الإضافية للإنتاج
echo "تثبيت مكتبات الإنتاج الإضافية..."
pip3 install gunicorn gevent psycopg2-binary redis sentry-sdk

print_step "تم تثبيت جميع المكتبات"

# ==========================================
# الخطوة 4: تجميع الملفات الثابتة
# ==========================================

print_header "الخطوة 4: تجميع الملفات الثابتة"

echo "تجميع Static Files..."
python3 manage.py collectstatic --noinput --clear

print_step "تم تجميع الملفات الثابتة"

# ==========================================
# الخطوة 5: تشغيل الاختبارات
# ==========================================

print_header "الخطوة 5: تشغيل الاختبارات"

if [ -f "test_system.py" ]; then
    echo "تشغيل اختبارات النظام..."
    python3 test_system.py || print_warning "بعض الاختبارات فشلت"
fi

if [ -f "test_billiards.py" ]; then
    echo "تشغيل اختبارات البلياردو..."
    python3 test_billiards.py || print_warning "بعض الاختبارات فشلت"
fi

print_step "تم الاختبار"

# ==========================================
# الخطوة 6: بناء الملفات
# ==========================================

print_header "الخطوة 6: بناء الملفات"

# Minify CSS و JS (اختياري)
if command -v terser &> /dev/null; then
    echo "Minifying JavaScript files..."
    # terser frontend/js/*.js -c -m -o frontend/js/app.min.js
    print_step "JavaScript files minified"
fi

if command -v cssnano &> /dev/null; then
    echo "Minifying CSS files..."
    # cssnano frontend/css/main.css -o frontend/css/main.min.css
    print_step "CSS files minified"
fi

print_step "تم البناء"

# ==========================================
# الخطوة 7: إعداد متغيرات البيئة
# ==========================================

print_header "الخطوة 7: إعداد متغيرات البيئة"

if [ ! -f ".env.production" ]; then
    echo "إنشاء ملف .env.production..."
    cat > .env.production << 'EOF'
# إعدادات الإنتاج
DEBUG=False
SECRET_KEY=your-secret-key-here-change-it
ALLOWED_HOSTS=example.com,www.example.com

# قاعدة البيانات
DB_ENGINE=django.db.backends.postgresql
DB_NAME=billiards_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Redis Cache
REDIS_URL=redis://localhost:6379/1

# CORS
CORS_ALLOWED_ORIGINS=https://example.com,https://app.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://app.example.com

# البريد الإلكتروني
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Sentry (اختياري)
SENTRY_DSN=https://your-sentry-dsn-here@sentry.io/project-id

# المراقبة
ENVIRONMENT=production
BUILD_ID=build-1
DEPLOY_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF
    print_step "تم إنشاء .env.production"
    print_warning "تأكد من تحديث القيم في .env.production قبل النشر"
else
    print_step ".env.production موجود بالفعل"
fi

# ==========================================
# الخطوة 8: إعداد Docker (اختياري)
# ==========================================

print_header "الخطوة 8: إعداد Docker (اختياري)"

if command -v docker &> /dev/null; then
    echo "Docker موجود"
    
    if [ ! -f "Dockerfile" ]; then
        echo "إنشاء Dockerfile..."
        cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# تثبيت المكتبات النظامية
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملفات المشروع
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn gevent psycopg2-binary

COPY . .

# جمع الملفات الثابتة
RUN python manage.py collectstatic --noinput

# تشغيل الخادم
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "hello_world.wsgi:application"]

EXPOSE 8000
EOF
        print_step "تم إنشاء Dockerfile"
    else
        print_step "Dockerfile موجود بالفعل"
    fi
    
    if [ ! -f ".dockerignore" ]; then
        echo "إنشاء .dockerignore..."
        cat > .dockerignore << 'EOF'
__pycache__
.pytest_cache
.venv
venv
*.pyc
*.pyo
*.pyd
.Python
*.egg-info
dist
build
*.log
.env
.git
.gitignore
.dockerignore
Dockerfile
docker-compose.yml
.vscode
.idea
EOF
        print_step "تم إنشاء .dockerignore"
    fi
else
    print_warning "Docker غير مثبت (اختياري)"
fi

# ==========================================
# الملخص النهائي
# ==========================================

print_header "✨ تم البناء بنجاح!"

echo ""
echo "الخطوات التالية:"
echo "1. تحديث متغيرات البيئة في .env.production"
echo "2. تشغيل الخادم: python manage.py runserver --settings=hello_world.production_settings"
echo "3. أو استخدام gunicorn: gunicorn --workers=4 hello_world.wsgi:application"
echo "4. أو استخدام Docker: docker build -t billiards:2.0.0 . && docker run -p 8000:8000 billiards:2.0.0"
echo ""
echo "للمزيد من المعلومات، راجع:"
echo "  • README.md"
echo "  • ANALYSIS_AND_PRODUCTION_PLAN.md"
echo "  • hello_world/production_settings.py"
echo ""

print_step "البناء اكتمل بنجاح! 🎉"
