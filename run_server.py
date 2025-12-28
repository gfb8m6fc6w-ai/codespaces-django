#!/usr/bin/env python3
"""
تطبيق خادم بسيط بدون FastAPI - نسخة بديلة
يعمل مع المكتبات المثبتة بالفعل
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import sys
import logging

# إعداد السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent))

try:
    from backend.billiards.engine import BilliardsEngine
    from backend.billiards.calculator import ShotCalculator
    from backend.models.shot import Shot, Difficulty
    logger.info("✅ تم استيراد جميع المكتبات بنجاح")
except ImportError as e:
    logger.error(f"❌ خطأ في الاستيراد: {e}")
    sys.exit(1)

# تهيئة محرك البلياردو
try:
    engine = BilliardsEngine()
    calculator = ShotCalculator()
    logger.info("✅ محرك البلياردو تم تهيئته")
except Exception as e:
    logger.error(f"❌ خطأ في تهيئة المحرك: {e}")
    sys.exit(1)


class BilliardsAPIHandler(BaseHTTPRequestHandler):
    """معالج طلبات HTTP"""
    
    def do_GET(self):
        """معالجة طلبات GET"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        try:
            # المسار الرئيسي
            if path == '/':
                response = {
                    "message": "مرحباً بك في 5A Diamond System Pro API",
                    "version": "2.0.0",
                    "status": "جاهز للخدمة",
                    "endpoints": {
                        "health": "/health",
                        "calculate": "/api/v1/calculate",
                        "statistics": "/api/v1/statistics",
                        "shots": "/api/v1/shots",
                    }
                }
                self.send_response(200)
            
            # فحص الصحة
            elif path == '/health':
                response = {
                    "status": "healthy",
                    "uptime": "جاهز",
                    "total_shots": len(engine.shots),
                    "total_calculations": engine.statistics.total_calculations,
                    "success_rate": round(engine.statistics.success_rate, 2),
                }
                self.send_response(200)
            
            # الحصول على التسديقات
            elif path == '/api/v1/shots':
                rails = query_params.get('rails', [None])[0]
                difficulty = query_params.get('difficulty', [None])[0]
                
                shots = engine.shots
                if rails:
                    shots = [s for s in shots if s.rails == int(rails)]
                if difficulty:
                    shots = [s for s in shots if s.difficulty.value == difficulty]
                
                response = {
                    "total": len(shots),
                    "shots": [s.to_dict() for s in shots],
                }
                self.send_response(200)
            
            # الإحصائيات
            elif path == '/api/v1/statistics':
                response = engine.get_statistics()
                self.send_response(200)
            
            # إحصائيات حسب الجدران
            elif path == '/api/v1/statistics/by-rails':
                stats = {}
                for rails in [1, 2, 3, 4]:
                    shots = engine.get_shots_by_rails(rails)
                    if shots:
                        successful = sum(1 for s in shots if s.executed and s.result)
                        stats[f"rails_{rails}"] = {
                            "total": len(shots),
                            "successful": successful,
                            "success_rate": round((successful / len(shots)) * 100, 2) if shots else 0,
                        }
                response = stats
                self.send_response(200)
            
            else:
                response = {"error": "المسار غير موجود"}
                self.send_response(404)
            
            # إرسال الرد
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الطلب: {e}")
            response = {"error": str(e)}
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """معالجة طلبات POST"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        try:
            # حساب تسديقة
            if path == '/api/v1/calculate':
                try:
                    rails = int(query_params.get('rails', [1])[0])
                    cue_position = float(query_params.get('cue_position', [5])[0])
                    white_ball = float(query_params.get('white_ball', [3])[0])
                    target = float(query_params.get('target', [2])[0])
                    pocket = int(query_params.get('pocket', [3])[0])
                    
                    shot = engine.calculate_shot(rails, cue_position, white_ball, target, pocket)
                    summary = calculator.get_calculation_summary(shot)
                    
                    response = {
                        "success": True,
                        "shot": shot.to_dict(),
                        "summary": summary,
                    }
                    self.send_response(200)
                except ValueError as e:
                    response = {"error": str(e)}
                    self.send_response(400)
            
            # تسجيل نتيجة
            elif path.startswith('/api/v1/shots/') and path.endswith('/record'):
                try:
                    shot_id = int(path.split('/')[4])
                    successful = query_params.get('successful', ['true'])[0].lower() == 'true'
                    
                    if shot_id < 0 or shot_id >= len(engine.shots):
                        raise ValueError("التسديقة غير موجودة")
                    
                    shot = engine.shots[shot_id]
                    engine.record_execution(shot, successful)
                    
                    response = {
                        "success": True,
                        "message": "تم تسجيل النتيجة بنجاح",
                    }
                    self.send_response(200)
                except (ValueError, IndexError) as e:
                    response = {"error": str(e)}
                    self.send_response(400)
            
            # تصدير البيانات
            elif path == '/api/v1/export':
                response = {
                    "shots": [s.to_dict() for s in engine.shots],
                    "statistics": engine.get_statistics(),
                }
                self.send_response(200)
            
            else:
                response = {"error": "المسار غير موجود"}
                self.send_response(404)
            
            # إرسال الرد
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            logger.error(f"❌ خطأ في معالجة الطلب: {e}")
            response = {"error": str(e)}
            self.send_response(500)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        """معالجة طلبات OPTIONS (CORS)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """تخصيص رسائل السجل"""
        logger.info(format % args)


def main():
    """تشغيل الخادم"""
    host = '0.0.0.0'
    port = 8001
    
    server = HTTPServer((host, port), BilliardsAPIHandler)
    
    print("=" * 70)
    print("🚀 خادم 5A Diamond System Pro جاهز")
    print("=" * 70)
    print(f"📡 الرابط: http://localhost:{port}")
    print(f"🌐 العناوين:")
    print(f"   • الرئيسية: http://localhost:{port}/")
    print(f"   • الصحة:   http://localhost:{port}/health")
    print(f"   • حساب:    http://localhost:{port}/api/v1/calculate")
    print(f"   • احصائيات: http://localhost:{port}/api/v1/statistics")
    print("=" * 70)
    print("⏹️  اضغط Ctrl+C للإيقاف")
    print("=" * 70)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ تم إيقاف الخادم بنجاح")
        sys.exit(0)


if __name__ == "__main__":
    main()
