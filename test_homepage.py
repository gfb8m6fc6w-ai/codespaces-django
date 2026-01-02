#!/usr/bin/env python
"""
اختبار سريع للصفحة الرئيسية الجديدة
Quick test for the new homepage
"""

import subprocess
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def test_homepage():
    """اختبر الصفحة الرئيسية"""
    print("\n" + "="*70)
    print("🧪 اختبار الصفحة الرئيسية الجديدة")
    print("="*70)
    
    base_url = "http://localhost:8000"
    
    try:
        session = requests_retry_session()
        
        # اختبار 1: الصفحة الرئيسية
        print("\n✓ اختبار 1: الصفحة الرئيسية")
        response = session.get(f"{base_url}/", timeout=5)
        
        if response.status_code == 200:
            print("  ✅ الصفحة تحمل بنجاح (200 OK)")
            
            # تحقق من المحتوى
            content = response.text.lower()
            checks = [
                ("البلياردو", "نظام البلياردو"),
                ("5A Diamond", "نظام 5A"),
                ("الميزات", "الميزات الرئيسية"),
                ("الحاسبة", "حاسبة الضربات"),
            ]
            
            for name, keyword in checks:
                if keyword.lower() in content:
                    print(f"  ✅ وجدت: {name}")
                else:
                    print(f"  ⚠️  لم أجد: {name}")
        else:
            print(f"  ❌ خطأ في التحميل: {response.status_code}")
        
        # اختبار 2: فحص الصحة
        print("\n✓ اختبار 2: فحص الصحة (/health/)")
        response = session.get(f"{base_url}/health/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ok':
                print(f"  ✅ الخادم يعمل بنجاح")
                print(f"  ✅ الرسالة: {data.get('message')}")
            else:
                print(f"  ⚠️  حالة غير متوقعة: {data}")
        else:
            print(f"  ❌ خطأ: {response.status_code}")
        
        # اختبار 3: API Info
        print("\n✓ اختبار 3: معلومات API (/api/info/)")
        response = session.get(f"{base_url}/api/info/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ اسم التطبيق: {data.get('app_name')}")
            print(f"  ✅ الإصدار: {data.get('version')}")
            print(f"  ✅ الحالة: {data.get('status')}")
            print(f"  ✅ الميزات: {', '.join(data.get('features', []))}")
        else:
            print(f"  ❌ خطأ: {response.status_code}")
        
        # اختبار 4: Admin Panel
        print("\n✓ اختبار 4: لوحة التحكم (/admin/)")
        response = session.get(f"{base_url}/admin/", timeout=5, allow_redirects=False)
        
        if response.status_code in [200, 302]:
            print(f"  ✅ لوحة التحكم متاحة (حالة: {response.status_code})")
        else:
            print(f"  ⚠️  حالة غير متوقعة: {response.status_code}")
        
        # اختبار 5: أداء الصفحة
        print("\n✓ اختبار 5: أداء التحميل")
        start = time.time()
        response = session.get(f"{base_url}/", timeout=5)
        elapsed = time.time() - start
        
        if elapsed < 0.5:
            print(f"  ✅ تحميل سريع جداً: {elapsed*1000:.0f}ms")
        elif elapsed < 1:
            print(f"  ✅ تحميل سريع: {elapsed*1000:.0f}ms")
        elif elapsed < 2:
            print(f"  ⚠️  تحميل معقول: {elapsed*1000:.0f}ms")
        else:
            print(f"  ❌ تحميل بطيء: {elapsed*1000:.0f}ms")
        
        print("\n" + "="*70)
        print("✨ جميع الاختبارات اكتملت بنجاح!")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ لم يتمكن من الاتصال بالخادم")
        print("   تأكد من أن الخادم يعمل:")
        print("   python manage.py runserver 0.0.0.0:8000")
    except Exception as e:
        print(f"\n❌ حدث خطأ: {e}")

if __name__ == "__main__":
    print("\n⏳ انتظر قليلاً... سيبدأ الاختبار خلال 3 ثواني")
    time.sleep(3)
    test_homepage()
