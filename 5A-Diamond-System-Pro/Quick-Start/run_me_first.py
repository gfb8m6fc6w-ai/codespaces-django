#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت البدء السريع
Quick Start Script for 5A Diamond System Pro
"""

import sys
import os
from pathlib import Path

def print_header(title):
    """طباعة رأس جميل"""
    print("\n" + "=" * 60)
    print(f"  🎱 {title}")
    print("=" * 60 + "\n")

def print_success(msg):
    """طباعة رسالة نجاح"""
    print(f"✅ {msg}")

def print_info(msg):
    """طباعة معلومة"""
    print(f"ℹ️  {msg}")

def print_error(msg):
    """طباعة رسالة خطأ"""
    print(f"❌ {msg}")

def check_python_version():
    """التحقق من إصدار Python"""
    print_header("التحقق من متطلبات النظام")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (مطلوب 3.8+)")
        return False

def check_dependencies():
    """التحقق من التبعيات"""
    print_header("التحقق من التبعيات")
    
    required = ['json', 'pathlib', 'datetime']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print_success(f"✓ {package}")
        except ImportError:
            print_error(f"✗ {package}")
            missing.append(package)
    
    return len(missing) == 0

def setup_directories():
    """إنشاء المجلدات الضرورية"""
    print_header("إعداد المجلدات")
    
    dirs = [
        'data',
        'logs',
        'cache',
        'Pythonista-iOS/data',
        'PWA-Web/assets',
        'Python-Backend/logs'
    ]
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        print_success(f"✓ {dir_name}/")
    
    return True

def create_config_files():
    """إنشاء ملفات الإعدادات"""
    print_header("إنشاء ملفات الإعدادات")
    
    config_content = """{
    "app_name": "5A Diamond System Pro",
    "version": "1.0.0",
    "debug": true,
    "storage": {
        "type": "local",
        "path": "./data"
    },
    "api": {
        "host": "localhost",
        "port": 8000
    }
}
"""
    
    config_path = Path('config.json')
    config_path.write_text(config_content, encoding='utf-8')
    print_success("✓ config.json")
    
    return True

def show_next_steps():
    """عرض الخطوات التالية"""
    print_header("الخطوات التالية")
    
    print("""
1️⃣  تشغيل على الويب:
   - افتح: PWA-Web/index.html في المتصفح
   - أو: python -m http.server 8000

2️⃣  تشغيل على iPhone:
   - انسخ: Pythonista-iOS/billiards_app.py
   - شغل التطبيق من Pythonista

3️⃣  تشغيل الخادم:
   - python Python-Backend/api.py
   - سيعمل على: http://localhost:8000

4️⃣  اقرأ الوثائق:
   - دليل المستخدم: Documentation/USER_GUIDE_AR.md
   - دليل المطور: Documentation/DEVELOPER_GUIDE.md

5️⃣  ابدأ بحساب التسديقات!
   """)

def main():
    """الدالة الرئيسية"""
    print_header("5A Diamond System Pro - البدء السريع")
    
    # التحقق من المتطلبات
    if not check_python_version():
        print_error("لا يمكن المتابعة بدون Python 3.8+")
        sys.exit(1)
    
    if not check_dependencies():
        print_error("بعض التبعيات المطلوبة غير مثبتة")
        # لا نتوقف، قد تكون اختيارية
    
    # إعداد المجلدات
    if not setup_directories():
        print_error("فشل إنشاء المجلدات")
        sys.exit(1)
    
    # إنشاء الملفات
    if not create_config_files():
        print_error("فشل إنشاء ملفات الإعدادات")
        sys.exit(1)
    
    # عرض الخطوات التالية
    show_next_steps()
    
    print_success("\n🎉 تم الإعداد بنجاح! استمتع بالتطبيق\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  تم الإيقاف من قبل المستخدم")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        sys.exit(1)
