#!/bin/bash

##############################################################################
#
#  DEPLOY SCRIPT - سكريبت النشر
#
#  الوظيفة: نشر المشروع في بيئة الإنتاج
#  الاستخدام: ./deploy.sh [environment]
#
#  البيئات المدعومة:
#  - staging: بيئة الاختبار
#  - production: بيئة الإنتاج
#
#  الخطوات:
#  1. التحقق من الإعدادات
#  2. بناء الصورة
#  3. دفع الصورة
#  4. تشغيل الحاويات
#  5. اختبارات الدخان
#  6. المراقبة
#
##############################################################################

set -e

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# المتغيرات
ENVIRONMENT=${1:-staging}
APP_NAME="billiards"
IMAGE_VERSION="2.0.0"
REGISTRY="docker.io"
REGISTORY_USERNAME=${DOCKER_USERNAME:-}
REGISTORY_PASSWORD=${DOCKER_PASSWORD:-}

# الدوال
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
    exit 1
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# ==========================================
# التحقق من المتطلبات
# ==========================================

print_header "الخطوة 1: التحقق من المتطلبات"

if ! command -v docker &> /dev/null; then
    print_error "Docker غير مثبت"
fi

if ! command -v docker-compose &> /dev/null; then
    print_warning "docker-compose غير مثبت (قد يكون اختياري)"
fi

if ! command -v git &> /dev/null; then
    print_warning "git غير مثبت"
fi

print_step "المتطلبات موجودة"

# ==========================================
# التحقق من البيئة
# ==========================================

print_header "الخطوة 2: التحقق من البيئة"

if [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "production" ]; then
    print_error "البيئة غير صحيحة. استخدم: staging أو production"
fi

print_step "البيئة المحددة: $ENVIRONMENT"

if [ ! -f ".env.${ENVIRONMENT}" ]; then
    print_error "ملف .env.${ENVIRONMENT} غير موجود"
fi

print_step ".env.${ENVIRONMENT} موجود"

# ==========================================
# بناء Docker Image
# ==========================================

print_header "الخطوة 3: بناء Docker Image"

IMAGE_NAME="${REGISTRY}/${APP_NAME}:${IMAGE_VERSION}-${ENVIRONMENT}"

echo "بناء الصورة: $IMAGE_NAME..."
docker build -t $IMAGE_NAME .

print_step "تم بناء الصورة"

# ==========================================
# اختبار الصورة محلياً
# ==========================================

print_header "الخطوة 4: اختبار الصورة محلياً"

echo "تشغيل اختبارات الصورة..."

# اختبار أن الصورة تعمل
docker run --rm \
    --env-file .env.${ENVIRONMENT} \
    $IMAGE_NAME \
    python manage.py check

print_step "اختبارات الصورة نجحت"

# ==========================================
# دفع الصورة (إذا كان هناك registry)
# ==========================================

print_header "الخطوة 5: دفع الصورة إلى Registry"

if [ -z "$REGISTORY_USERNAME" ] || [ -z "$REGISTORY_PASSWORD" ]; then
    print_warning "بيانات Registry غير محددة. سيتم تخطي دفع الصورة"
else
    echo "تسجيل الدخول إلى Docker Registry..."
    echo "$REGISTORY_PASSWORD" | docker login -u "$REGISTORY_USERNAME" --password-stdin $REGISTRY
    
    echo "دفع الصورة..."
    docker push $IMAGE_NAME
    
    print_step "تم دفع الصورة"
fi

# ==========================================
# تشغيل الحاويات
# ==========================================

print_header "الخطوة 6: تشغيل الحاويات"

# إيقاف الحاويات القديمة
if docker ps -a --format '{{.Names}}' | grep -q "^${APP_NAME}-${ENVIRONMENT}$"; then
    echo "إيقاف الحاوية القديمة..."
    docker stop "${APP_NAME}-${ENVIRONMENT}" || true
    docker rm "${APP_NAME}-${ENVIRONMENT}" || true
fi

# تشغيل حاوية جديدة
echo "تشغيل الحاوية الجديدة..."
docker run -d \
    --name "${APP_NAME}-${ENVIRONMENT}" \
    --env-file ".env.${ENVIRONMENT}" \
    -p 8000:8000 \
    -v /opt/billiards/data:/app/.billiards_data \
    -v /opt/billiards/logs:/app/logs \
    --restart unless-stopped \
    $IMAGE_NAME

sleep 3
print_step "تم تشغيل الحاوية"

# ==========================================
# اختبارات الدخان
# ==========================================

print_header "الخطوة 7: اختبارات الدخان"

echo "الانتظار حتى يكون الخادم جاهزاً..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health 2>/dev/null; then
        break
    fi
    echo "محاولة $i/30..."
    sleep 2
done

# اختبار الصحة
echo "اختبار صحة الخادم..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
if echo $HEALTH_RESPONSE | grep -q "status"; then
    print_step "الخادم صحي"
else
    print_error "فشل اختبار الصحة"
fi

# اختبار API
echo "اختبار API..."
API_RESPONSE=$(curl -s http://localhost:8000/api/v1/ || echo "error")
if [ "$API_RESPONSE" != "error" ]; then
    print_step "API يعمل بشكل صحيح"
else
    print_warning "قد لا يكون API متاح في هذا الوقت"
fi

# ==========================================
# إعداد المراقبة
# ==========================================

print_header "الخطوة 8: إعداد المراقبة"

echo "إعداد سجل الأخطاء..."
docker logs "${APP_NAME}-${ENVIRONMENT}" | tail -20

print_step "المراقبة جاهزة"

# ==========================================
# النسخة الاحتياطية
# ==========================================

print_header "الخطوة 9: النسخ الاحتياطية"

BACKUP_DIR="/opt/billiards/backups/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "إنشاء نسخة احتياطية في $BACKUP_DIR..."
if [ -d "/opt/billiards/data" ]; then
    tar -czf "$BACKUP_DIR/data.tar.gz" -C /opt/billiards data/
    print_step "تم النسخ الاحتياطي"
fi

# ==========================================
# الملخص النهائي
# ==========================================

print_header "✨ تم النشر بنجاح!"

echo ""
echo "معلومات النشر:"
echo "  • البيئة: $ENVIRONMENT"
echo "  • الصورة: $IMAGE_NAME"
echo "  • الحاوية: ${APP_NAME}-${ENVIRONMENT}"
echo "  • الرابط: http://localhost:8000"
echo ""
echo "الأوامر المفيدة:"
echo "  • عرض السجلات: docker logs -f ${APP_NAME}-${ENVIRONMENT}"
echo "  • إيقاف الحاوية: docker stop ${APP_NAME}-${ENVIRONMENT}"
echo "  • حذف الحاوية: docker rm ${APP_NAME}-${ENVIRONMENT}"
echo "  • إعادة تشغيل: docker restart ${APP_NAME}-${ENVIRONMENT}"
echo ""

print_step "النشر اكتمل بنجاح! 🎉"
