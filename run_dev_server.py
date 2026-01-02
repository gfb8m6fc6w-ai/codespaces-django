#!/usr/bin/env python
"""
سكريبت تشغيل خادم التطوير المحسّن
Enhanced Development Server Script
مصمم للعمل مع Codespaces و iPad
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header(text):
    """طباعة رأس جميل"""
    print("\n" + "="*70)
    print(f"🚀 {text}")
    print("="*70)

def print_success(text):
    """طباعة رسالة نجاح"""
    print(f"✅ {text}")

def print_warning(text):
    """طباعة تحذير"""
    print(f"⚠️  {text}")

def print_error(text):
    """طباعة خطأ"""
    print(f"❌ {text}")

def check_env_file():
    """التحقق من ملف .env"""
    if not os.path.exists('.env'):
        print_warning("ملف .env غير موجود!")
        print("📝 جاري إنشاء ملف .env...")
        with open('.env', 'w') as f:
            f.write("""# إعدادات Django
SECRET_KEY=kakgox-korno4-cytPyk
DEBUG=True
ALLOWED_HOSTS=*

# إعدادات قاعدة البيانات
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=""
DB_USERNAME=""
DB_PASSWORD=""
""")
        print_success("تم إنشاء ملف .env")
    else:
        print_success("ملف .env موجود")

def check_dependencies():
    """التحقق من المكتبات"""
    print("\n📦 التحقق من المكتبات...")
    required = {
        'django': 'Django',
        'decouple': 'python-decouple',
        'rest_framework': 'djangorestframework',
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
            print_success(f"{package}")
        except ImportError:
            print_warning(f"{package} غير موجود")
            missing.append(package)
    
    if missing:
        print(f"\n🔧 تثبيت المكتبات الناقصة: {', '.join(missing)}")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print_success("جميع المكتبات موجودة!")

def run_migrations():
    """تطبيق الهجرات"""
    print("\n🔄 تطبيق هجرات قاعدة البيانات...")
    result = subprocess.run(
        [sys.executable, "manage.py", "migrate", "--noinput"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print_success("الهجرات تمت بنجاح")
    else:
        print_warning(f"قد تكون هناك مشاكل: {result.stderr[:100]}")

def collect_static():
    """جمع الملفات الثابتة"""
    print("\n📂 جمع الملفات الثابتة...")
    result = subprocess.run(
        [sys.executable, "manage.py", "collectstatic", "--noinput"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print_success("الملفات الثابتة جاهزة")
    else:
        print_warning("قد تكون هناك مشاكل في الملفات الثابتة")

def main():
    """الدالة الرئيسية"""
    print_header("خادم Django للتطوير - محسّن لـ Codespaces و iPad")
    
    # التحقق من الإعدادات
    check_env_file()
    check_dependencies()
    run_migrations()
    collect_static()
    
    # الخادم جاهز
    print_header("✨ كل شيء جاهز! الخادم سيبدأ الآن")
    
    print("\n📌 معلومات مهمة:")
    print("   🌐 URL المحلي:  http://localhost:8000")
    print("   🌐 URL العام:    http://0.0.0.0:8000")
    print("   📱 من iPad:      انسخ الرابط من Codespaces")
    print("   🔑 Admin Panel:   http://localhost:8000/admin/")
    print("   ❤️  Health Check: http://localhost:8000/health/")
    
    print("\n⌚ انتظر 2 ثانية قبل بدء الخادم...")
    time.sleep(2)
    
    print("\n" + "="*70)
    print("💡 للإيقاف: اضغط Ctrl + C")
    print("="*70 + "\n")
    
    # تشغيل الخادم
    try:
        os.execvp(
            sys.executable, 
            [sys.executable, "manage.py", "runserver", "0.0.0.0:8000"]
        )
    except KeyboardInterrupt:
        print("\n\n👋 تم إيقاف الخادم")
        sys.exit(0)

if __name__ == "__main__":
    main()
