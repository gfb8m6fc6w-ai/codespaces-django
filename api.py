"""
API REST محسّن باستخدام FastAPI أو بديل HTTP بسيط
يوفر واجهة موحدة لجميع أنظمة البلياردو

الاستخدام:
  python api.py          # إذا كانت FastAPI مثبتة
  python run_server.py   # إذا لم تكن FastAPI مثبتة
"""

import json
from pathlib import Path
import logging
import sys

# إعداد السجل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent))

# ==========================================
# استيراد المكتبات المطلوبة
# ==========================================

try:
    from backend.billiards.engine import BilliardsEngine
    from backend.billiards.calculator import ShotCalculator
    from backend.models.shot import Shot, Difficulty
    logger.info("✅ تم استيراد مكتبات البلياردو بنجاح")
except ImportError as e:
    logger.error(f"❌ خطأ في استيراد المكتبات: {e}")
    print("\n⚠️ خطأ: لم يتم العثور على المكتبات المطلوبة")
    print("   تأكد من تثبيت المتطلبات:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

# محاولة استيراد FastAPI
FASTAPI_AVAILABLE = False
try:
    from fastapi import FastAPI, HTTPException, File, UploadFile, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
    from typing import List, Optional
    
    FASTAPI_AVAILABLE = True
    logger.info("✅ FastAPI متاح")
    
except ImportError:
    logger.warning("⚠️ FastAPI غير مثبت")
    logger.info("   للتثبيت: pip install fastapi uvicorn")
    logger.info("   أو استخدم: python run_server.py")

# ==========================================
# تهيئة محرك البلياردو
# ==========================================

try:
    engine = BilliardsEngine()
    calculator = ShotCalculator()
    logger.info("✅ محرك البلياردو تم تهيئته بنجاح")
except Exception as e:
    logger.error(f"❌ خطأ في تهيئة المحرك: {e}")
    sys.exit(1)


# ==========================================
# إنشاء تطبيق FastAPI
# ==========================================

if FASTAPI_AVAILABLE:
    
    app = FastAPI(
        title="5A Diamond System Pro API",
        description="API احترافي لنظام تحليل تسديدات البلياردو",
        version="2.0.0",
    )
    
    # إضافة CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # ==========================================
    # المسارات الأساسية
    # ==========================================

    @app.get("/")
    async def root():
        """المسار الرئيسي - معلومات API"""
        return {
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


    @app.get("/health")
    async def health_check():
        """فحص صحة الخادم"""
        try:
            return {
                "status": "healthy",
                "uptime": "جاهز",
                "total_shots": len(engine.shots),
                "total_calculations": engine.statistics.total_calculations,
                "success_rate": round(engine.statistics.success_rate, 2),
            }
        except Exception as e:
            logger.error(f"❌ خطأ في فحص الصحة: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    # ==========================================
    # حساب التسديقات
    # ==========================================

    @app.post("/api/v1/calculate")
    async def calculate_shot(
        rails: int = Query(..., ge=1, le=4, description="عدد الجدران"),
        cue_position: float = Query(..., ge=0, le=10, description="موضع العصا"),
        white_ball: float = Query(..., ge=0, le=10, description="موضع الكرة البيضاء"),
        target: float = Query(..., ge=0, le=10, description="موضع الهدف"),
        pocket: int = Query(..., ge=0, le=5, description="موضع الجيب"),
    ):
        """حساب تسديقة جديدة مع جميع المعاملات"""
        try:
            shot = engine.calculate_shot(rails, cue_position, white_ball, target, pocket)
            summary = calculator.get_calculation_summary(shot)
            
            logger.info(f"✅ تم حساب تسديقة: {rails} جدران، صعوبة {shot.difficulty.value}")
            
            return {
                "success": True,
                "shot": shot.to_dict(),
                "summary": summary,
            }
        except ValueError as e:
            logger.warning(f"⚠️ خطأ في المدخلات: {e}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"❌ خطأ في الحساب: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    # ==========================================
    # إدارة التسديقات
    # ==========================================

    @app.get("/api/v1/shots")
    async def get_shots(
        rails: Optional[int] = Query(None, ge=1, le=4, description="تصفية حسب الجدران"),
        difficulty: Optional[str] = Query(None, description="تصفية حسب الصعوبة"),
        skip: int = Query(0, ge=0, description="عدد العناصر المتخطاة"),
        limit: int = Query(100, ge=1, le=500, description="حد أقصى للعناصر"),
    ):
        """الحصول على قائمة التسديقات مع التصفية والترقيم"""
        try:
            shots = engine.shots
            
            # تصفية حسب الجدران
            if rails:
                shots = [s for s in shots if s.rails == rails]
            
            # تصفية حسب الصعوبة
            if difficulty:
                shots = [s for s in shots if s.difficulty.value == difficulty]
            
            # ترقيم الصفحات
            total = len(shots)
            shots = shots[skip:skip + limit]
            
            return {
                "total": total,
                "count": len(shots),
                "skip": skip,
                "limit": limit,
                "shots": [s.to_dict() for s in shots],
            }
        except Exception as e:
            logger.error(f"❌ خطأ في استرجاع التسديقات: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    @app.get("/api/v1/shots/{shot_id}")
    async def get_shot_by_id(shot_id: int):
        """الحصول على تسديقة محددة"""
        try:
            if shot_id < 0 or shot_id >= len(engine.shots):
                raise HTTPException(status_code=404, detail="التسديقة غير موجودة")
            
            return engine.shots[shot_id].to_dict()
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ خطأ في استرجاع التسديقة: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    @app.post("/api/v1/shots/{shot_id}/record")
    async def record_shot_execution(shot_id: int, successful: bool):
        """تسجيل نتيجة تنفيذ تسديقة"""
        try:
            if shot_id < 0 or shot_id >= len(engine.shots):
                raise HTTPException(status_code=404, detail="التسديقة غير موجودة")
            
            shot = engine.shots[shot_id]
            engine.record_execution(shot, successful)
            
            logger.info(f"✅ تم تسجيل النتيجة: {'نجاح' if successful else 'فشل'}")
            
            return {
                "success": True,
                "message": "تم تسجيل النتيجة بنجاح",
                "shot": shot.to_dict(),
            }
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"❌ خطأ في التسجيل: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    # ==========================================
    # الإحصائيات
    # ==========================================

    @app.get("/api/v1/statistics")
    async def get_statistics():
        """الحصول على الإحصائيات الكاملة"""
        try:
            stats = engine.get_statistics()
            logger.debug("✅ تم استرجاع الإحصائيات")
            return stats
        except Exception as e:
            logger.error(f"❌ خطأ في استرجاع الإحصائيات: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    @app.get("/api/v1/statistics/by-rails")
    async def get_statistics_by_rails():
        """الإحصائيات حسب عدد الجدران"""
        try:
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
            
            return stats
        except Exception as e:
            logger.error(f"❌ خطأ في الإحصائيات: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    @app.get("/api/v1/statistics/by-difficulty")
    async def get_statistics_by_difficulty():
        """الإحصائيات حسب مستوى الصعوبة"""
        try:
            stats = {}
            for difficulty in Difficulty:
                shots = engine.get_shots_by_difficulty(difficulty.value)
                if shots:
                    successful = sum(1 for s in shots if s.executed and s.result)
                    stats[difficulty.value] = {
                        "total": len(shots),
                        "successful": successful,
                        "success_rate": round((successful / len(shots)) * 100, 2) if shots else 0,
                    }
            
            return stats
        except Exception as e:
            logger.error(f"❌ خطأ في الإحصائيات: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    # ==========================================
    # استيراد وتصدير البيانات
    # ==========================================

    @app.post("/api/v1/export")
    async def export_data():
        """تصدير جميع البيانات"""
        try:
            data = {
                "shots": [s.to_dict() for s in engine.shots],
                "statistics": engine.get_statistics(),
            }
            logger.info(f"✅ تم تصدير {len(engine.shots)} تسديقة")
            return data
        except Exception as e:
            logger.error(f"❌ خطأ في التصدير: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    @app.post("/api/v1/import")
    async def import_data(file: UploadFile = File(...)):
        """استيراد البيانات من ملف JSON"""
        try:
            content = await file.read()
            data = json.loads(content.decode('utf-8'))
            
            # التحقق من صحة البيانات
            if 'shots' not in data:
                raise ValueError("الملف يجب أن يحتوي على 'shots'")
            
            # مسح البيانات الحالية
            engine.shots = []
            
            # استيراد التسديقات
            for shot_data in data['shots']:
                try:
                    shot = Shot.from_dict(shot_data)
                    engine.shots.append(shot)
                except Exception as e:
                    logger.warning(f"⚠️ تم تخطي تسديقة غير صحيحة: {e}")
            
            engine.save_to_storage()
            
            logger.info(f"✅ تم استيراد {len(engine.shots)} تسديقة")
            
            return {
                "success": True,
                "message": f"تم استيراد {len(engine.shots)} تسديقة بنجاح",
                "imported_count": len(engine.shots),
            }
        except json.JSONDecodeError as e:
            logger.error(f"❌ خطأ في صيغة JSON: {e}")
            raise HTTPException(status_code=400, detail="الملف يجب أن يكون بصيغة JSON صحيحة")
        except Exception as e:
            logger.error(f"❌ خطأ في الاستيراد: {e}")
            raise HTTPException(status_code=400, detail=str(e))


    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        """معالج الأخطاء العام"""
        logger.error(f"❌ خطأ غير متوقع: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "حدث خطأ غير متوقع"},
        )


if __name__ == "__main__":
    if FASTAPI_AVAILABLE:
        try:
            import uvicorn
            logger.info("🚀 بدء خادم FastAPI...")
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=8001,
                log_level="info",
            )
        except ImportError:
            logger.error("❌ uvicorn غير مثبت")
            logger.info("   للتثبيت: pip install uvicorn")
            logger.info("   أو استخدم: python run_server.py")
            sys.exit(1)
        except Exception as e:
            logger.error(f"❌ خطأ في بدء الخادم: {e}")
            sys.exit(1)
    else:
        logger.error("❌ FastAPI غير مثبت")
        logger.info("\nالخيارات المتاحة:")
        logger.info("1️⃣  تثبيت FastAPI: pip install fastapi uvicorn")
        logger.info("2️⃣  استخدام خادم بديل: python run_server.py")
        sys.exit(1)
