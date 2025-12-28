FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# إعداد البيئة
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# تثبيت المكتبات النظامية
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    postgresql-client \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت المكتبات Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install gunicorn gevent psycopg2-binary redis sentry-sdk

# نسخ المشروع
COPY . .

# إنشاء مجلدات مهمة
RUN mkdir -p /app/logs /app/.billiards_data /app/staticfiles

# جمع الملفات الثابتة
RUN python manage.py collectstatic --noinput --clear || true

# إضافة صحة الفحص
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# تعريض المنفذ
EXPOSE 8000

# تشغيل Gunicorn
CMD ["gunicorn", \
     "--workers=4", \
     "--worker-class=gevent", \
     "--bind=0.0.0.0:8000", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "--timeout=120", \
     "--keep-alive=5", \
     "hello_world.wsgi:application"]
