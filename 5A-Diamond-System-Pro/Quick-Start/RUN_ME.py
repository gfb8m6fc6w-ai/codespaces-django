#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 سكريبت البدء السريع
نقطة الدخول الرئيسية لتطبيق البلياردو
"""

def main():
    print("=" * 70)
    print("🎯 نظام البلياردو المتكامل 5A Diamond System Pro")
    print("=" * 70)
    print("\n📋 الخيارات المتاحة:\n")
    
    options = {
        '1': {
            'name': 'نسخة Pythonista iOS المتقدمة',
            'file': 'Pythonista-iOS/billiards_app_advanced.py',
            'desc': 'التطبيق الموحد الكامل مع جميع الميزات'
        },
        '2': {
            'name': 'نسخة Pythonista iOS الأساسية',
            'file': 'Pythonista-iOS/billiards_app.py',
            'desc': 'تطبيق بسيط وخفيف الوزن'
        },
        '3': {
            'name': 'تطبيق PWA الويب',
            'file': 'PWA-Web/index.html',
            'desc': 'تطبيق ويب متطور يعمل بدون إنترنت'
        },
        '4': {
            'name': 'حاسبة سريعة',
            'file': 'PWA-Web/billiards-calculator.html',
            'desc': 'حاسبة بسيطة وسريعة'
        },
        '5': {
            'name': 'تشغيل جميع الاختبارات',
            'file': 'tests',
            'desc': 'اختبر جميع الميزات'
        },
        '6': {
            'name': 'عرض الإحصائيات',
            'file': 'stats',
            'desc': 'عرض إحصائيات المشروع'
        }
    }
    
    for key, option in options.items():
        print(f"{key}. {option['name']}")
        print(f"   └─ {option['desc']}\n")
    
    print("\n" + "=" * 70)
    choice = input("اختر رقماً (1-6): ").strip()
    
    if choice == '1':
        run_pythonista_advanced()
    elif choice == '2':
        run_pythonista_basic()
    elif choice == '3':
        run_web_app()
    elif choice == '4':
        run_calculator()
    elif choice == '5':
        run_tests()
    elif choice == '6':
        show_statistics()
    else:
        print("❌ خيار غير صحيح")

def run_pythonista_advanced():
    """تشغيل نسخة Pythonista المتقدمة"""
    print("\n🚀 جاري تشغيل نسخة Pythonista المتقدمة...")
    try:
        exec(open('Pythonista-iOS/billiards_app_advanced.py').read())
    except Exception as e:
        print(f"❌ خطأ: {e}")

def run_pythonista_basic():
    """تشغيل نسخة Pythonista الأساسية"""
    print("\n🚀 جاري تشغيل نسخة Pythonista الأساسية...")
    try:
        exec(open('Pythonista-iOS/billiards_app.py').read())
    except Exception as e:
        print(f"❌ خطأ: {e}")

def run_web_app():
    """تشغيل تطبيق الويب"""
    print("\n🌐 فتح تطبيق الويب...")
    import webbrowser
    import os
    
    file_path = os.path.abspath('PWA-Web/index.html')
    webbrowser.open('file://' + file_path)
    print(f"✅ تم فتح: {file_path}")

def run_calculator():
    """تشغيل الحاسبة السريعة"""
    print("\n🧮 فتح الحاسبة السريعة...")
    import webbrowser
    import os
    
    file_path = os.path.abspath('PWA-Web/billiards-calculator.html')
    webbrowser.open('file://' + file_path)
    print(f"✅ تم فتح: {file_path}")

def run_tests():
    """تشغيل الاختبارات"""
    print("\n🧪 جاري تشغيل الاختبارات...")
    import subprocess
    import os
    
    test_files = [
        '../tests/test_calculator.py',
        '../test_system.py',
        '../test_billiards.py'
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n✅ تشغيل {test_file}...")
            try:
                subprocess.run(['python3', test_file])
            except Exception as e:
                print(f"❌ خطأ في {test_file}: {e}")
        else:
            print(f"⏭️  {test_file} غير موجود")

def show_statistics():
    """عرض إحصائيات المشروع"""
    print("\n📊 إحصائيات المشروع")
    print("=" * 70)
    
    import os
    import json
    from pathlib import Path
    
    base_path = Path('.')
    
    # عد الملفات
    py_files = list(base_path.rglob('*.py'))
    html_files = list(base_path.rglob('*.html'))
    js_files = list(base_path.rglob('*.js'))
    css_files = list(base_path.rglob('*.css'))
    json_files = list(base_path.rglob('*.json'))
    md_files = list(base_path.rglob('*.md'))
    
    print(f"\n📈 إحصائيات الملفات:")
    print(f"  • ملفات Python: {len(py_files)}")
    print(f"  • ملفات HTML: {len(html_files)}")
    print(f"  • ملفات JavaScript: {len(js_files)}")
    print(f"  • ملفات CSS: {len(css_files)}")
    print(f"  • ملفات JSON: {len(json_files)}")
    print(f"  • ملفات Markdown: {len(md_files)}")
    print(f"  • إجمالي الملفات: {len(py_files) + len(html_files) + len(js_files) + len(css_files) + len(json_files) + len(md_files)}")
    
    # حجم المشروع
    total_size = 0
    for file in base_path.rglob('*'):
        if file.is_file():
            total_size += file.stat().st_size
    
    print(f"\n💾 حجم المشروع: {total_size / 1024 / 1024:.2f} MB")
    
    # معلومات النسخة
    print(f"\n📦 معلومات النسخة:")
    print(f"  • الإصدار: 3.0.0")
    print(f"  • التاريخ: يناير 2026")
    print(f"  • الحالة: جاهز للإنتاج ✅")
    
    print("\n" + "=" * 70)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 تم الخروج")
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
