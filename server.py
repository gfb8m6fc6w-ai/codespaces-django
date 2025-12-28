#!/usr/bin/env python3
"""
خادم محلي لتطبيق 5A Diamond System Pro
الاستخدام: python3 server.py
ثم افتح: http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
import time
from pathlib import Path

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # إضافة رؤوس PWA
        self.send_header('Service-Worker-Allowed', '/')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # تحسين رسائل السجل
        client_ip = self.client_address[0]
        request_line = args[0] if args else 'Unknown'
        print(f"📡 {client_ip} - {request_line}")

def main():
    os.chdir(DIRECTORY)
    
    print("=" * 60)
    print("🚀 خادم 5A Diamond System Pro جاهز")
    print("=" * 60)
    print(f"📂 المسار: {DIRECTORY}")
    print(f"🌐 الرابط: http://localhost:{PORT}")
    print("=" * 60)
    print("📌 اضغط Ctrl+C للإيقاف")
    print("=" * 60)
    
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"\n✅ الخادم يعمل على http://localhost:{PORT}")
            print("⏳ جاري فتح المتصفح...")
            
            # فتح المتصفح تلقائياً بعد ثانية واحدة
            time.sleep(1)
            try:
                webbrowser.open(f'http://localhost:{PORT}')
            except Exception as e:
                print(f"⚠️ لم يتمكن من فتح المتصفح تلقائياً: {e}")
                print(f"افتح المتصفح يدويًا على: http://localhost:{PORT}")
            
            httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("\n\n⏹️ تم إيقاف الخادم")
        print("=" * 60)
    
    except Exception as e:
        print(f"\n❌ خطأ: {e}")
        print("تأكد من أن المنفذ 8000 غير مستخدم")

if __name__ == '__main__':
    main()
