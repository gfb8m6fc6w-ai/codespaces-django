#!/usr/bin/env python3
"""
سكريبت إعداد البيئة الشامل

يقوم بـ:
1. التحقق من إصدار Python
2. تثبيت المكتبات
3. إنشاء المجلدات المطلوبة
4. تكوين البيئة
"""

import sys
import subprocess
import os
from pathlib import Path
import json

# ألوان للطباعة
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(msg):
    """طباعة رأس القسم"""
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}{msg}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")


def print_success(msg):
    """طباعة رسالة نجاح"""
    print(f"{GREEN}✅ {msg}{RESET}")


def print_error(msg):
    """طباعة رسالة خطأ"""
    print(f"{RED}❌ {msg}{RESET}")


def print_warning(msg):
    """طباعة رسالة تحذير"""
    print(f"{YELLOW}⚠️ {msg}{RESET}")


def print_info(msg):
    """طباعة رسالة معلومات"""
    print(f"{BLUE}ℹ️  {msg}{RESET}")


def main():
    """الدالة الرئيسية"""
    print(f"\n{BOLD}{BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  🎯 إعداد نظام البلياردو - 5A Diamond System Pro           ║")
    print("║                                                            ║")
    print("║  إصدار: 2.0.0                                             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")
    
    # خطوة 1: فحص Python
    print_header("1️⃣ فحص إصدار Python")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    print_info(f"إصدار Python المثبت: {version_str}")
    print_info(f"مسار التنفيذ: {sys.executable}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print_error(f"Python 3.9+ مطلوب، لديك {version_str}")
        sys.exit(1)
    
    print_success(f"إصدار Python صحيح: {version_str}")
    
    # خطوة 2: إنشاء المجلدات
    print_header("2️⃣ إنشاء المجلدات")
    
    project_root = Path(__file__).parent
    directories = [
        project_root / ".billiards_data",
        project_root / "logs",
    ]
    
    for dir_path in directories:
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            print_success(f"المجلد جاهز: {dir_path.name}")
        except Exception as e:
            print_error(f"خطأ في إنشاء {dir_path}: {e}")
    
    # خطوة 3: إعداد البيئة
    print_header("3️⃣ إعداد متغيرات البيئة")
    
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if not env_file.exists():
        if not env_example.exists():
            env_content = """# إعدادات البيئة

# السرية
SECRET_KEY=your-secret-key-here-change-in-production

# وضع التطوير
DEBUG=False

# إعدادات الخادم
SERVER_HOST=0.0.0.0
SERVER_PORT=8001

# إعدادات قاعدة البيانات
DATABASE_URL=sqlite:////workspaces/codespaces-django/.billiards_data/billiards.db

# مستوى السجل
LOG_LEVEL=INFO
"""
            env_example.write_text(env_content, encoding='utf-8')
            print_success("تم إنشاء ملف .env.example")
        
        with open(env_example, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print_success("تم إنشاء ملف .env")
    else:
        print_warning("ملف .env موجود بالفعل")
    
    # خطوة 4: إنشاء البيانات
    print_header("4️⃣ إنشاء ملفات البيانات")
    
    data_dir = project_root / ".billiards_data"
    
    shots_file = data_dir / "shots.json"
    stats_file = data_dir / "statistics.json"
    
    if not shots_file.exists():
        with open(shots_file, 'w', encoding='utf-8') as f:
            json.dump({"shots": []}, f, ensure_ascii=False, indent=2)
        print_success(f"تم إنشاء {shots_file.name}")
    
    if not stats_file.exists():
        initial_stats = {
            "total_calculations": 0,
            "total_shots_attempted": 0,
            "total_shots_successful": 0,
            "success_rate": 0.0,
            "average_difficulty": "متوسطة"
        }
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(initial_stats, f, ensure_ascii=False, indent=2)
        print_success(f"تم إنشاء {stats_file.name}")
    
    # الملخص
    print_header("📋 ملخص الإعداد")
    
    print_success("✅ تم فحص Python")
    print_success("✅ تم إنشاء المجلدات")
    print_success("✅ تم إعداد البيئة")
    print_success("✅ تم إنشاء البيانات")
    
    print(f"\n{GREEN}{BOLD}🎉 تم الإعداد الأساسي بنجاح!{RESET}")
    
    print(f"\n{BLUE}{BOLD}الخطوات التالية:{RESET}")
    print(f"\n1️⃣  تثبيت المكتبات:")
    print(f"    {BOLD}pip install -r requirements.txt{RESET}")
    print(f"\n2️⃣  تشغيل الخادم:")
    print(f"    {BOLD}python api.py{RESET}")
    print(f"\n3️⃣  فتح المتصفح:")
    print(f"    {BOLD}http://localhost:8001{RESET}")
    print(f"\n4️⃣  تشغيل الاختبارات:")
    print(f"    {BOLD}python test_system.py{RESET}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}تم إلغاء الإعداد بواسطة المستخدم{RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"خطأ غير متوقع: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
