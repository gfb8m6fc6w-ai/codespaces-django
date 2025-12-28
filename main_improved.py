"""
API REST محسّن بـ معالجة أخطاء قوية وأداء عالي
"""

from fastapi import FastAPI, HTTPException, File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import List, Optional
import json
from pathlib import Path
import sys
import logging
from datetime import datetime

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from billiards.engine_improved import BilliardsEngine
    from billiards.calculator_improved import ShotCalculator
except ImportError:
    from billiards.engine import BilliardsEngine
    from billiards.calculator import ShotCalculator

from models.shot import Shot, Difficulty

# إعداد Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# إنشاء تطبيق FastAPI
app = FastAPI(
    title="5A Diamond System Pro API - محسّن",
    description="API محسّن لتطبيق نظام البلياردو الاحترافي",
    version="1.0.1",
)

# إضافة CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تهيئة محرك البلياردو
try:
    engine = BilliardsEngine()
    calculator = ShotCalculator()
    logger.info("✅ تم تهيئة محرك البلياردو بنجاح")
except Exception as e:
    logger.error(f"❌ خطأ في تهيئة محرك البلياردو: {e}")
    raise


# ========================================
# دوال مساعدة
# ========================================

def safe_save_storage():
    """حفظ آمن للبيانات"""
    try:
        if hasattr(engine, 'save_to_storage'):
            engine.save_to_storage()
    except Exception as e:
        logger.warning(f"⚠️ تحذير: لم يتمكن من حفظ البيانات: {e}")


def get_shots_by_rails(rails: int) -> List:
    """الحصول على التسديقات حسب الجدران"""
    return [s for s in engine.shots if s.rails == rails]


def get_performance_stats() -> dict:
    """الحصول على إحصائيات الأداء"""
    try:
        if hasattr(engine, 'get_performance_stats'):
            return engine.get_performance_stats()
        return {
            "total_shots": len(engine.shots),
            "cache_size": len(getattr(calculator, '_difficulty_cache', {})),
            "memory_info": "N/A"
        }
    except Exception as e:
        logger.warning(f"⚠️ خطأ في الحصول على إحصائيات الأداء: {e}")
        return {}


# ========================================
# معالجات الأخطاء المخصصة
# ========================================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """معالج أخطاء القيم"""
    logger.error(f"❌ خطأ في القيمة: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "خطأ في القيمة",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request, exc):
    """معالج أخطاء التحقق من البيانات"""
    logger.error(f"❌ خطأ في التحقق: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "خطأ في التحقق من البيانات",
            "details": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """معالج الأخطاء العامة"""
    logger.error(f"❌ خطأ غير متوقع: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "خطأ في الخادم",
            "message": "حدث خطأ غير متوقع",
            "timestamp": datetime.now().isoformat()
        }
    )


# ========================================
# المسارات الأساسية
# ========================================

@app.get("/")
async def root():
    """المسار الرئيسي"""
    logger.info("📌 تم الوصول للصفحة الرئيسية")
    return {
        "message": "مرحباً بك في 5A Diamond System Pro API - النسخة المحسّنة",
        "version": "1.0.1",
        "features": {
            "billiards_engine": "✅ محرك بلياردو احترافي",
            "caching": "✅ نظام caching متقدم",
            "logging": "✅ نظام logging احترافي",
            "error_handling": "✅ معالجة أخطاء قوية"
        },
        "endpoints": {
            "health": "/health",
            "calculate": "/api/v1/calculate",
            "statistics": "/api/v1/statistics",
            "shots": "/api/v1/shots",
            "performance": "/api/v1/performance"
        }
    }


@app.get("/health")
async def health_check():
    """فحص صحة الخادم مع معلومات التفاصيل"""
    try:
        logger.info("🏥 فحص صحة الخادم")
        stats = engine.get_statistics() if hasattr(engine, 'get_statistics') else {}
        
        total_calculations = getattr(engine, 'statistics', {})
        if hasattr(total_calculations, 'total_calculations'):
            total_calculations = total_calculations.total_calculations
        else:
            total_calculations = 0
        
        cache_size = len(getattr(calculator, '_difficulty_cache', {}))
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "total_shots": len(engine.shots),
                "total_calculations": total_calculations,
                "success_rate": stats.get('success_rate', 0),
                "cache_size": cache_size
            }
        }
    except Exception as e:
        logger.error(f"❌ خطأ في فحص الصحة: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الخادم")


# ========================================
# حساب التسديقات
# ========================================

@app.post("/api/v1/calculate")
async def calculate_shot(
    rails: int = Query(..., ge=1, le=4, description="عدد الجدران"),
    cue_position: float = Query(..., ge=0, le=10, description="موضع العصا"),
    white_ball: float = Query(..., ge=0, le=10, description="موضع الكرة البيضاء"),
    target: float = Query(..., ge=0, le=10, description="موضع الهدف"),
    pocket: int = Query(..., ge=0, le=5, description="موضع الجيب"),
):
    """
    حساب تسديدة جديدة مع معالجة أخطاء محسّنة
    
    Parameters:
    - rails: عدد الجدران (1-4)
    - cue_position: موضع العصا (0-10)
    - white_ball: موضع الكرة البيضاء (0-10)
    - target: موضع الهدف (0-10)
    - pocket: موضع الجيب المستهدف (0-5)
    """
    try:
        logger.info(f"📊 حساب تسديدة جديدة: جدران={rails}")
        
        shot = engine.calculate_shot(rails, cue_position, white_ball, target, pocket)
        summary = calculator.get_calculation_summary(shot)
        safe_save_storage()
        
        logger.info(f"✅ تم حساب التسديدة بنجاح")
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "shot": shot.to_dict(),
            "summary": summary,
        }
    
    except ValueError as e:
        logger.warning(f"⚠️ خطأ في المعاملات: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ خطأ في حساب التسديدة: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الحساب")


# ========================================
# إدارة التسديقات
# ========================================

@app.get("/api/v1/shots")
async def get_shots(
    rails: Optional[int] = Query(None, ge=1, le=4, description="تصفية حسب الجدران"),
    difficulty: Optional[str] = Query(None, description="تصفية حسب الصعوبة"),
    limit: int = Query(100, ge=1, le=1000, description="الحد الأقصى للنتائج")
):
    """
    الحصول على قائمة التسديقات مع التصفية والتقييد
    """
    try:
        logger.info(f"📋 استرجاع التسديقات")
        
        shots = list(engine.shots)
        
        if rails:
            shots = [s for s in shots if getattr(s, 'rails', None) == rails]
        
        if difficulty:
            shots = [s for s in shots if getattr(getattr(s, 'difficulty', None), 'value', None) == difficulty]
        
        # تطبيق الحد الأقصى
        shots = shots[-limit:]
        
        logger.info(f"✅ تم استرجاع {len(shots)} تسديدة")
        
        return {
            "total": len(shots),
            "limit": limit,
            "timestamp": datetime.now().isoformat(),
            "shots": [s.to_dict() for s in shots],
        }
    
    except Exception as e:
        logger.error(f"❌ خطأ في استرجاع التسديقات: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الاسترجاع")


@app.get("/api/v1/shots/{shot_id}")
async def get_shot_by_id(shot_id: int):
    """
    الحصول على تسديدة محددة برقمها
    """
    try:
        if shot_id < 0 or shot_id >= len(engine.shots):
            logger.warning(f"⚠️ تسديدة غير موجودة: #{shot_id}")
            raise HTTPException(status_code=404, detail="لم يتم العثور على التسديدة")
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "shot": engine.shots[shot_id].to_dict()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ خطأ في استرجاع التسديدة: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الاسترجاع")


@app.post("/api/v1/shots/{shot_id}/record")
async def record_shot_execution(shot_id: int, successful: bool):
    """
    تسجيل نتيجة تنفيذ تسديدة
    """
    try:
        if shot_id < 0 or shot_id >= len(engine.shots):
            raise HTTPException(status_code=404, detail="لم يتم العثور على التسديدة")
        
        shot = engine.shots[shot_id]
        if hasattr(engine, 'record_execution'):
            engine.record_execution(shot, successful)
        else:
            shot.executed = True
            shot.result = successful
        
        safe_save_storage()
        
        logger.info(f"✅ تم تسجيل نتيجة التسديدة #{shot_id}")
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "message": "تم تسجيل النتيجة بنجاح",
            "shot": shot.to_dict(),
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ خطأ في تسجيل النتيجة: {e}")
        raise HTTPException(status_code=500, detail="خطأ في التسجيل")


# ========================================
# الإحصائيات والأداء
# ========================================

@app.get("/api/v1/statistics")
async def get_statistics():
    """
    الحصول على الإحصائيات الكاملة
    """
    try:
        logger.info("📊 استرجاع الإحصائيات")
        stats = engine.get_statistics()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "statistics": stats
        }
    
    except Exception as e:
        logger.error(f"❌ خطأ في استرجاع الإحصائيات: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الإحصائيات")


@app.get("/api/v1/statistics/by-rails")
async def get_statistics_by_rails():
    """
    الإحصائيات حسب عدد الجدران
    """
    try:
        logger.info("📊 استرجاع الإحصائيات حسب الجدران")
        stats = {}
        difficulty_map = {"سهلة": 1, "متوسطة": 2, "صعبة": 3, "جداً صعبة": 4, "قصوى": 5}
        
        for rails in [1, 2, 3, 4]:
            shots = get_shots_by_rails(rails)
            if shots:
                successful = sum(1 for s in shots if getattr(s, 'executed', False) and getattr(s, 'result', False))
                
                difficulty_values = []
                for s in shots:
                    diff_obj = getattr(s, 'difficulty', None)
                    if diff_obj is not None:
                        diff_value = getattr(diff_obj, 'value', 'متوسطة')
                        difficulty_values.append(difficulty_map.get(diff_value, 3))
                    else:
                        difficulty_values.append(3)
                
                avg_difficulty = sum(difficulty_values) / len(difficulty_values) if difficulty_values else 0
                
                stats[f"rails_{rails}"] = {
                    "total": len(shots),
                    "successful": successful,
                    "success_rate": (successful / len(shots)) * 100 if shots else 0,
                    "average_difficulty": round(avg_difficulty, 2)
                }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "statistics": stats
        }
    
    except Exception as e:
        logger.error(f"❌ خطأ في استرجاع الإحصائيات: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الإحصائيات")


@app.get("/api/v1/performance")
async def get_performance():
    """
    الحصول على إحصائيات الأداء والذاكرة
    """
    try:
        logger.info("⚡ استرجاع إحصائيات الأداء")
        perf = get_performance_stats()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "performance": perf
        }
    
    except Exception as e:
        logger.error(f"❌ خطأ في استرجاع إحصائيات الأداء: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الأداء")


# ========================================
# استيراد وتصدير البيانات
# ========================================

@app.post("/api/v1/export")
async def export_data():
    """
    تصدير جميع البيانات
    """
    try:
        logger.info("📤 تصدير البيانات")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "shots": [s.to_dict() for s in engine.shots],
            "statistics": engine.get_statistics() if hasattr(engine, 'get_statistics') else {},
        }
    
    except Exception as e:
        logger.error(f"❌ خطأ في التصدير: {e}")
        raise HTTPException(status_code=500, detail="خطأ في التصدير")


@app.post("/api/v1/import")
async def import_data(file: UploadFile = File(...)):
    """
    استيراد البيانات من ملف JSON
    """
    try:
        logger.info("📥 استيراد البيانات")
        
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
                engine.shots.append(Shot.from_dict(shot_data))
            except Exception as e:
                logger.warning(f"⚠️ خطأ في استيراد تسديدة: {e}")
        
        safe_save_storage()
        
        logger.info(f"✅ تم استيراد {len(engine.shots)} تسديدة")
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "message": f"تم استيراد {len(engine.shots)} تسديدة",
        }
    
    except json.JSONDecodeError:
        logger.error("❌ الملف ليس JSON صحيح")
        raise HTTPException(status_code=400, detail="الملف يجب أن يكون JSON")
    except ValueError as e:
        logger.error(f"❌ خطأ في صحة البيانات: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ خطأ في الاستيراد: {e}")
        raise HTTPException(status_code=500, detail="خطأ في الاستيراد")


@app.delete("/api/v1/data/cleanup")
async def cleanup_old_data(days: int = Query(30, ge=1, le=365)):
    """
    حذف البيانات القديمة
    """
    try:
        logger.info(f"🗑️ تنظيف البيانات الأقدم من {days} يوم")
        
        cutoff_date = datetime.now().timestamp() - (days * 86400)
        deleted_count = 0
        
        # حذف التسديقات القديمة
        original_count = len(engine.shots)
        engine.shots = [
            s for s in engine.shots
            if getattr(s, 'timestamp', None) is None or float(getattr(s, 'timestamp', 0)) > cutoff_date
        ]
        deleted_count = original_count - len(engine.shots)
        
        safe_save_storage()
        
        logger.info(f"✅ تم حذف {deleted_count} تسديقة قديمة")
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "deleted_count": deleted_count,
            "message": f"تم حذف {deleted_count} تسديدة قديمة"
        }
    
    except Exception as e:
        logger.error(f"❌ خطأ في التنظيف: {e}")
        raise HTTPException(status_code=500, detail="خطأ في التنظيف")


if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 بدء خادم API محسّن")
    uvicorn.run(app, host="0.0.0.0", port=8001)
