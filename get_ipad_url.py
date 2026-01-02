#!/usr/bin/env python
"""
الحصول على الرابط الصحيح للدخول من iPad
Get the correct URL for iPad access
"""

import os
import socket
import subprocess

def get_codespace_url():
    """الحصول على URL Codespaces الصحيح"""
    print("\n" + "="*70)
    print("📱 الحصول على رابط الدخول من iPad")
    print("="*70)
    
    # محاولة الحصول على متغيرات البيئة
    codespace_name = os.environ.get('CODESPACE_NAME')
    domain = os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')
    
    if codespace_name and domain:
        # الرابط الكامل لـ Codespaces
        url = f"https://{codespace_name}-8000.{domain}/"
        print(f"\n✅ رابط Codespaces:")
        print(f"   {url}")
        
    else:
        print("\n⚠️  متغيرات Codespaces غير محددة")
        print("   هذا طبيعي في بيئة التطوير المحلية")
    
    # الرابط المحلي
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(f"\n✅ الرابط المحلي (نفس الجهاز فقط):")
        print(f"   http://localhost:8000/")
        print(f"   http://127.0.0.1:8000/")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    print("\n" + "="*70)
    print("📋 خطوات الاستخدام على iPad:")
    print("="*70)
    print("""
1. 🌐 افتح Safari على iPad
2. 📋 انسخ أحد الروابط أعلاه
3. 📌 الصقها في شريط العنوان
4. ⏎ اضغط على زر الدخول
5. ✅ ستشاهد الصفحة الرئيسية

📱 نصيحة: حفظ الرابط كإشارة مرجعية لسهولة الوصول
""")

if __name__ == "__main__":
    get_codespace_url()
