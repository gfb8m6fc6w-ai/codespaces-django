# 📱 دليل الإنتاج والتصدير لأجهزة الآيباد
## نظام البلياردو المتقدم - 5A Diamond System Pro

---

## 🚀 البدء السريع

### المتطلبات
- Docker و Docker Compose (للإنتاج)
- Python 3.11+ (للتطوير)
- PostgreSQL 15+ (اختياري - قاعدة بيانات الإنتاج)
- Redis 7+ (اختياري - تخزين مؤقت)
- Nginx (اختياري - reverse proxy)

### التثبيت السريع

#### 1. باستخدام Docker (مُوصى به)
```bash
# بناء الصورة
docker build -t billiards:2.0.0 .

# تشغيل التطبيق
docker run -d \
  --name billiards-app \
  -p 8000:8000 \
  --env-file .env.production \
  billiards:2.0.0
```

#### 2. باستخدام Docker Compose (الخيار الكامل)
```bash
# بدء جميع الخدمات
docker-compose up -d

# التحقق من الحالة
docker-compose ps

# إيقاف الخدمات
docker-compose down
```

#### 3. التثبيت اليدوي (التطوير)
```bash
# تثبيت المكتبات
pip install -r requirements.txt

# تهيئة قاعدة البيانات
python manage.py migrate

# تجميع الملفات الثابتة
python manage.py collectstatic

# تشغيل الخادم
python manage.py runserver --settings=hello_world.production_settings
```

---

## 📝 ملفات الإعدادات

### متغيرات البيئة الأساسية

إنشاء ملف `.env.production`:

```bash
# إعدادات Django
DEBUG=False
SECRET_KEY=your-very-long-secret-key-change-it-immediately
ALLOWED_HOSTS=example.com,www.example.com,app.example.com

# قاعدة البيانات (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=billiards_db
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=db  # إذا كنت تستخدم Docker
DB_PORT=5432

# Redis Cache
REDIS_URL=redis://cache:6379/1  # أو redis://localhost:6379/1

# CORS والأمان
CORS_ALLOWED_ORIGINS=https://example.com,https://app.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://app.example.com

# البريد الإلكتروني
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@example.com

# Sentry (مراقبة الأخطاء)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id

# التحديد الشخصي
ENVIRONMENT=production
BUILD_ID=build-001
DEPLOY_TIME=2025-12-28T10:00:00Z
```

---

## 🏗️ البناء والنشر

### خطوة 1: البناء

```bash
# منح صلاحيات التنفيذ
chmod +x build.sh deploy.sh

# بناء المشروع
./build.sh
```

**ما يفعله بناء.sh:**
- التحقق من المتطلبات
- تنظيف الملفات القديمة
- تثبيت المكتبات
- تجميع الملفات الثابتة
- تشغيل الاختبارات
- إنشاء ملفات الإنتاج

### خطوة 2: الاختبار

```bash
# اختبارات الوحدة
python -m pytest test_system.py -v

# اختبارات الأداء
python test_billiards.py

# اختبارات يدوية
curl http://localhost:8000/health
```

### خطوة 3: النشر

```bash
# النشر في بيئة Staging
./deploy.sh staging

# النشر في الإنتاج
./deploy.sh production
```

**ما يفعله النشر:**
- بناء Docker Image
- اختبار الصورة
- دفع للـ Registry (اختياري)
- تشغيل الحاويات
- اختبارات الدخان
- إعداد المراقبة
- النسخ الاحتياطية

---

## 📱 تحسينات الآيباد

### PWA Configuration

التطبيق مُعد بالكامل كـ PWA:

1. **manifest.json**: تم إنشاؤه بالفعل
2. **service-worker.js**: تم إنشاؤه بالفعل
3. **Icons**: أضف الأيقونات في `/static/images/`

### التثبيت على الآيباد

#### في Safari
1. افتح التطبيق في Safari
2. اضغط زر المشاركة (Share)
3. اختر "إضافة إلى الشاشة الرئيسية" (Add to Home Screen)
4. سيظهر التطبيق بدون واجهة Safari

#### في Chrome
1. افتح التطبيق في Chrome
2. اضغط القائمة (⋮)
3. اختر "تثبيت التطبيق" (Install app)

### متطلبات الأداء على الآيباد

```
✅ حجم الملفات الأولية: < 500KB
✅ وقت التحميل الأول: < 2 ثانية
✅ FPS سلس: 60 FPS
✅ استخدام الذاكرة: < 150MB
✅ عرض الشاشة: 768px - 1024px
✅ دعم Touch Optimization
```

---

## 🔒 الأمان

### قائمة التحقق من الأمان

- [ ] تفعيل HTTPS/SSL
- [ ] تغيير SECRET_KEY
- [ ] تعيين ALLOWED_HOSTS الصحيح
- [ ] تفعيل SECURE_SSL_REDIRECT
- [ ] تفعيل CSRF Protection
- [ ] تفعيل CORS بشكل صحيح
- [ ] تعيين CSP Headers
- [ ] تفعيل HSTS
- [ ] تعطيل DEBUG في الإنتاج
- [ ] استخدام متغيرات البيئة الآمنة

### SSL/TLS

#### باستخدام Let's Encrypt

```bash
# التثبيت
sudo apt-get install certbot python3-certbot-nginx

# الحصول على شهادة
sudo certbot certonly --standalone -d example.com

# التحديث التلقائي
sudo systemctl enable certbot.timer
```

#### باستخدام Docker

```bash
# استخدم صورة certbot
docker run -it --rm \
  -v /etc/letsencrypt:/etc/letsencrypt \
  -v /var/lib/letsencrypt:/var/lib/letsencrypt \
  certbot/certbot certonly --standalone -d example.com
```

---

## 📊 المراقبة والسجلات

### عرض السجلات

```bash
# Docker Logs
docker logs -f billiards-app

# File Logs
tail -f logs/django.log
tail -f logs/errors.log
```

### مراقبة الأداء

```bash
# استخدام Prometheus
docker run -p 9090:9090 prom/prometheus

# استخدام Grafana
docker run -p 3000:3000 grafana/grafana
```

### اختبارات الأداء

```bash
# استخدام Lighthouse
lighthouse https://example.com

# استخدام WebPageTest
# https://www.webpagetest.org/

# استخدام Chrome DevTools
# F12 -> Performance tab
```

---

## 🔄 النسخ الاحتياطية والاستعادة

### النسخ الاحتياطية التلقائية

```bash
# إنشاء سكريبت نسخ احتياطي
chmod +x backup.sh

# جدولة النسخ الاحتياطية (Cron)
0 2 * * * /path/to/backup.sh  # كل يوم الساعة 2 صباحاً
```

### نسخ احتياطية يدوية

```bash
# نسخ احتياطية قاعدة البيانات
docker exec billiards-db pg_dump -U postgres billiards_db > backup.sql

# نسخ احتياطية البيانات
tar -czf billiards_data_backup.tar.gz .billiards_data/

# استعادة قاعدة البيانات
docker exec -i billiards-db psql -U postgres billiards_db < backup.sql
```

---

## 🐛 استكشاف الأخطاء

### المشاكل الشائعة

#### 1. الخادم لا يستجيب

```bash
# التحقق من حالة الحاوية
docker ps -a

# عرض السجلات
docker logs billiards-app

# إعادة التشغيل
docker restart billiards-app
```

#### 2. قاعدة البيانات غير متاحة

```bash
# التحقق من قاعدة البيانات
docker exec billiards-db pg_isready -U postgres

# إعادة تشغيل
docker restart billiards-db
```

#### 3. الملفات الثابتة غير مرئية

```bash
# تجميع الملفات
python manage.py collectstatic --noinput

# التحقق من الصلاحيات
ls -la static/
```

#### 4. مشاكل الأداء

```bash
# مسح الـ Cache
docker exec billiards-cache redis-cli FLUSHALL

# مراقبة الموارد
docker stats

# اختبار الأداء
ab -n 1000 -c 10 http://localhost:8000/
```

---

## 📈 التحسينات المستقبلية

### المرحلة التالية

- [ ] إضافة Progressive Web App Icon
- [ ] تحسينات Dark Mode
- [ ] إضافة Multi-language Support
- [ ] تحسينات Offline Mode
- [ ] إضافة Push Notifications
- [ ] تحسينات الواجهة
- [ ] تحسينات الأداء الإضافية

---

## 📚 الموارد

### التوثيق
- [Django Documentation](https://docs.djangoproject.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Nginx Documentation](https://nginx.org/en/docs/)

### أدوات مفيدة
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [PageSpeed Insights](https://pagespeed.web.dev/)
- [GTmetrix](https://gtmetrix.com/)
- [WebPageTest](https://www.webpagetest.org/)

### أمان
- [OWASP Top 10](https://owasp.org/Top10/)
- [SSL Labs](https://www.ssllabs.com/ssltest/)
- [Security Headers](https://securityheaders.com/)

---

## 📞 الدعم والمساعدة

### للأسئلة والمشاكل

1. تحقق من [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. اطلع على السجلات (Logs)
3. راجع [README_FULL.md](README_FULL.md)
4. افتح issue على GitHub

---

## 📄 الترخيص

هذا المشروع مرخص تحت MIT License.

---

**آخر تحديث:** ٢٨ ديسمبر ٢٠٢٥  
**الإصدار:** 2.0.0  
**الحالة:** جاهز للإنتاج ✅
