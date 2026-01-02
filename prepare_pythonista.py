#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
أداة التحضير والتثبيت لـ Pythonista
Pythonista Preparation Tool

هذا الملف يقوم بـ:
1. إنشاء ملفات المشروع في شكل يسهل نسخها
2. إنشاء ملف HTML للتحميل المباشر
3. إنشاء تعليمات التثبيت
"""

import os
import json
from pathlib import Path
from datetime import datetime

def create_installation_package():
    """إنشاء حزمة التثبيت الكاملة"""
    
    # المسار الأساسي
    base_path = Path('/workspaces/codespaces-django')
    pythonista_dir = base_path / 'pythonista'
    pythonista_dir.mkdir(exist_ok=True)
    
    # الملفات المراد نسخها
    files_to_copy = [
        'pythonista_billiards_app.py',
        'pythonista_advanced_billiards.py',
        'PYTHONISTA_SETUP_GUIDE.md'
    ]
    
    # نسخ الملفات
    for filename in files_to_copy:
        source = base_path / filename
        if source.exists():
            with open(source, 'r', encoding='utf-8') as f:
                content = f.read()
            
            dest = pythonista_dir / filename
            with open(dest, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'✓ تم نسخ {filename}')

def create_quick_start_guide():
    """إنشاء دليل البدء السريع"""
    
    guide = """# دليل البدء السريع لـ Pythonista
# Quick Start Guide for Pythonista 3

## الطريقة الأسرع (٥ دقائق)

### 1️⃣ تثبيت Pythonista
- افتح App Store
- ابحث عن "Pythonista 3"
- اضغط تثبيت

### 2️⃣ نسخ الملف
**الخيار أ**: عبر iCloud
- حمّل `pythonista_billiards_app.py`
- ضعه في iCloud Drive
- افتح في Pythonista

**الخيار ب**: عبر البريد
- أرسل الملف لبريدك
- افتحه على iPhone
- اختر "نسخ إلى Pythonista"

### 3️⃣ تشغيل التطبيق
- اضغط على الملف
- اضغط زر التشغيل ▶

## 🎮 الاستخدام

```
الزاوية: -90 إلى 90 درجة
القوة: 0 إلى 100
المسافة: بالسنتيمتر
الصعوبة: اختر من القائمة
```

اضغط "حساب" واستمتع!

---

**نسخة متقدمة متوفرة**: pythonista_advanced_billiards.py
"""
    
    with open('/workspaces/codespaces-django/QUICK_START_PYTHONISTA.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print('✓ تم إنشاء دليل البدء السريع')

def create_installation_html():
    """إنشاء صفحة HTML للتحميل"""
    
    html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تثبيت تطبيق البلياردو على Pythonista</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
            padding-top: 40px;
        }
        
        h1 {
            font-size: 32px;
            margin-bottom: 10px;
            color: #16c784;
        }
        
        .subtitle {
            color: #aaa;
            font-size: 16px;
        }
        
        .section {
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #16c784;
        }
        
        h2 {
            color: #16c784;
            margin-bottom: 15px;
            font-size: 20px;
        }
        
        .step {
            display: flex;
            margin-bottom: 15px;
            align-items: flex-start;
        }
        
        .step-number {
            background: #16c784;
            color: #1a1a2e;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-left: 15px;
            flex-shrink: 0;
        }
        
        .step-content {
            flex: 1;
        }
        
        .step-content p {
            line-height: 1.6;
            color: #ddd;
        }
        
        .download-btn {
            display: block;
            background: #16c784;
            color: #1a1a2e;
            padding: 15px 30px;
            border-radius: 8px;
            text-decoration: none;
            text-align: center;
            font-weight: bold;
            margin: 20px 0;
            font-size: 16px;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }
        
        .download-btn:hover {
            background: #0fb370;
            transform: scale(1.05);
        }
        
        .feature-list {
            list-style: none;
        }
        
        .feature-list li {
            padding: 10px 0;
            padding-right: 25px;
            position: relative;
            color: #ddd;
        }
        
        .feature-list li:before {
            content: "✓";
            position: absolute;
            right: 0;
            color: #16c784;
            font-weight: bold;
            font-size: 18px;
        }
        
        .warning {
            background: rgba(233, 69, 96, 0.1);
            border-left-color: #e94560;
            margin: 20px 0;
        }
        
        .warning h3 {
            color: #e94560;
            margin-bottom: 10px;
        }
        
        .footer {
            text-align: center;
            color: #666;
            padding: 40px 0;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎱 حاسبة البلياردو</h1>
            <p class="subtitle">نسخة Pythonista المتقدمة</p>
        </header>
        
        <section class="section">
            <h2>📦 التثبيت في 5 دقائق</h2>
            
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <p><strong>ثبّت Pythonista 3</strong></p>
                    <p>من App Store على جهازك (مدفوع)</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <p><strong>حمّل الملف</strong></p>
                    <button class="download-btn" onclick="downloadFile('pythonista_billiards_app.py')">
                        ⬇️ تحميل التطبيق الأساسي
                    </button>
                    <button class="download-btn" onclick="downloadFile('pythonista_advanced_billiards.py')">
                        ⬇️ تحميل النسخة المتقدمة
                    </button>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <p><strong>انسخ الملف إلى Pythonista</strong></p>
                    <p>عبر iCloud Drive أو البريد الإلكتروني</p>
                </div>
            </div>
            
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <p><strong>اضغط على ▶</strong></p>
                    <p>وابدأ الاستخدام مباشرة</p>
                </div>
            </div>
        </section>
        
        <section class="section">
            <h2>✨ المميزات</h2>
            <ul class="feature-list">
                <li>حسابات متقدمة للتسديقات</li>
                <li>واجهة رسومية جميلة</li>
                <li>دعم كامل للغة العربية</li>
                <li>حفظ البيانات محلياً</li>
                <li>إحصائيات تفصيلية</li>
                <li>لا يحتاج إنترنت</li>
                <li>مجاني تماماً (بخلاف Pythonista نفسه)</li>
            </ul>
        </section>
        
        <section class="section warning">
            <h3>⚠️ متطلبات مهمة</h3>
            <p>Pythonista 3 هو تطبيق مدفوع على App Store (~$10)</p>
            <p>يُرجى التأكد من اتصالك بـ WiFi لأول مرة</p>
        </section>
        
        <section class="section">
            <h2>🆘 في حالة المشاكل</h2>
            <p><strong>المشكلة:</strong> الملف لا يفتح</p>
            <p><strong>الحل:</strong></p>
            <ol style="margin-right: 20px; margin-top: 10px;">
                <li>جرب نسخ الملف يدوياً</li>
                <li>أعد تشغيل Pythonista</li>
                <li>تأكد من iOS 12 أو أحدث</li>
            </ol>
        </section>
        
        <div class="footer">
            <p>© 2026 Billiards App | جميع الحقوق محفوظة</p>
        </div>
    </div>
    
    <script>
        function downloadFile(filename) {
            const link = document.createElement('a');
            link.href = `./${filename}`;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>
</body>
</html>
"""
    
    with open('/workspaces/codespaces-django/pythonista_installation.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print('✓ تم إنشاء صفحة HTML للتثبيت')

def create_info_file():
    """إنشاء ملف معلومات JSON"""
    
    info = {
        "app_name": "حاسبة البلياردو",
        "version": "1.0",
        "platform": "Pythonista 3",
        "supported_ios": "12.0+",
        "created_date": datetime.now().isoformat(),
        "files": {
            "basic": {
                "name": "pythonista_billiards_app.py",
                "description": "النسخة الأساسية - تطبيق بسيط وفعال",
                "size": "~15KB",
                "features": [
                    "حساب نسبة النجاح",
                    "واجهة رسومية",
                    "حفظ البيانات",
                    "إحصائيات أساسية"
                ]
            },
            "advanced": {
                "name": "pythonista_advanced_billiards.py",
                "description": "النسخة المتقدمة - مميزات إضافية",
                "size": "~40KB",
                "features": [
                    "تبويبات متعددة",
                    "حسابات متقدمة",
                    "توصيات ذكية",
                    "تحليل الأداء",
                    "إحصائيات شاملة"
                ]
            }
        },
        "installation_methods": [
            "iCloud Drive",
            "Email",
            "Web Server",
            "USB Transfer"
        ],
        "data_storage": "~/Documents/BilliardsApp/",
        "language": "العربية الكاملة",
        "internet_required": False,
        "paid_features": None,
        "support_email": "support@example.com"
    }
    
    with open('/workspaces/codespaces-django/pythonista_app_info.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    
    print('✓ تم إنشاء ملف المعلومات')

def main():
    """الدالة الرئيسية"""
    print("""
╔═════════════════════════════════════════════════╗
║   أداة تحضير Pythonista                        ║
║   Pythonista Preparation Tool                   ║
╚═════════════════════════════════════════════════╝
    """)
    
    print('جاري التحضير...')
    
    create_installation_package()
    create_quick_start_guide()
    create_installation_html()
    create_info_file()
    
    print("""
╔═════════════════════════════════════════════════╗
║   ✓ تم الانتهاء بنجاح!                        ║
╚═════════════════════════════════════════════════╝

الملفات المُنشأة:
1. pythonista_billiards_app.py - التطبيق الأساسي
2. pythonista_advanced_billiards.py - النسخة المتقدمة
3. PYTHONISTA_SETUP_GUIDE.md - دليل الإعداد الكامل
4. QUICK_START_PYTHONISTA.md - دليل البدء السريع
5. pythonista_installation.html - صفحة التثبيت
6. pythonista_app_info.json - معلومات التطبيق

خطوات التثبيت على Pythonista:
────────────────────────────────
1. ثبّت Pythonista 3 من App Store
2. احمل أحد الملفات أعلاه
3. انسخه إلى Pythonista عبر:
   • iCloud Drive
   • البريد الإلكتروني
   • Web Server
4. شغّل الملف باضغط على ▶

استمتع بتطبيقك! 🎱
    """)

if __name__ == '__main__':
    main()
