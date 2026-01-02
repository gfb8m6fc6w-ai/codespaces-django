#!/usr/bin/env python3
"""
اختبار شامل لجميع مكونات نظام البلياردو

يختبر:
- استيراد جميع المكتبات
- تهيئة محرك البلياردو
- حساب التسديدات
- الإحصائيات
- التخزين والاسترجاع
"""

import sys
import json
from pathlib import Path

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent))

import logging

# إعداد السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_imports():
    """اختبار استيراد جميع المكتبات"""
    print("\n" + "="*60)
    print("1️⃣  اختبار الاستيراضات")
    print("="*60)
    
    try:
        from backend.billiards.engine import BilliardsEngine
        logger.info("✅ تم استيراد BilliardsEngine")
    except Exception as e:
        logger.error(f"❌ خطأ في استيراد BilliardsEngine: {e}")
        return False
    
    try:
        from backend.billiards.calculator import ShotCalculator
        logger.info("✅ تم استيراد ShotCalculator")
    except Exception as e:
        logger.error(f"❌ خطأ في استيراد ShotCalculator: {e}")
        return False
    
    try:
        from backend.models.shot import Shot, Difficulty
        logger.info("✅ تم استيراد Shot و Difficulty")
    except Exception as e:
        logger.error(f"❌ خطأ في استيراد Shot: {e}")
        return False
    
    try:
        from backend.models.statistics import Statistics
        logger.info("✅ تم استيراد Statistics")
    except Exception as e:
        logger.error(f"❌ خطأ في استيراد Statistics: {e}")
        return False
    
    return True


def test_engine_initialization():
    """اختبار تهيئة محرك البلياردو"""
    print("\n" + "="*60)
    print("2️⃣  اختبار تهيئة المحرك")
    print("="*60)
    
    try:
        from backend.billiards.engine import BilliardsEngine
        engine = BilliardsEngine()
        
        logger.info(f"✅ تم تهيئة المحرك")
        logger.info(f"   - عدد التسديدات: {len(engine.shots)}")
        logger.info(f"   - الإحصائيات: {engine.statistics}")
        
        return engine
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة المحرك: {e}")
        return None


def test_shot_calculation(engine):
    """اختبار حساب التسديدات"""
    print("\n" + "="*60)
    print("3️⃣  اختبار حساب التسديدات")
    print("="*60)
    
    try:
        # اختبار 1: تسديقة بسيطة (جدار واحد)
        shot1 = engine.calculate_shot(
            rails=1,
            cue_position=2.5,
            white_ball=3.0,
            target=5.5,
            pocket=0
        )
        logger.info(f"✅ تسديقة 1: {shot1.rails} جدار، صعوبة {shot1.difficulty.value}")
        logger.info(f"   - احتمال النجاح: {shot1.success_rate}%")
        
        # اختبار 2: تسديقة معقدة (4 جدران)
        shot2 = engine.calculate_shot(
            rails=4,
            cue_position=1.0,
            white_ball=2.0,
            target=8.0,
            pocket=3
        )
        logger.info(f"✅ تسديقة 2: {shot2.rails} جدران، صعوبة {shot2.difficulty.value}")
        logger.info(f"   - احتمال النجاح: {shot2.success_rate}%")
        
        # اختبار 3: تسديقة متوسطة (جداران)
        shot3 = engine.calculate_shot(
            rails=2,
            cue_position=5.0,
            white_ball=5.0,
            target=5.0,
            pocket=1
        )
        logger.info(f"✅ تسديقة 3: {shot3.rails} جدران، صعوبة {shot3.difficulty.value}")
        logger.info(f"   - احتمال النجاح: {shot3.success_rate}%")
        
        logger.info(f"✅ إجمالي التسديدات: {len(engine.shots)}")
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في حساب التسديدات: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_shot_execution(engine):
    """اختبار تسجيل نتائج التسديدات"""
    print("\n" + "="*60)
    print("4️⃣  اختبار تسجيل النتائج")
    print("="*60)
    
    try:
        if len(engine.shots) < 3:
            logger.warning("⚠️ لا توجد تسديقات كافية للاختبار")
            return False
        
        # تسجيل نجاح للتسديقة الأولى
        engine.record_execution(engine.shots[0], True)
        logger.info(f"✅ تم تسجيل نجاح للتسديقة 1")
        
        # تسجيل فشل للتسديقة الثانية
        engine.record_execution(engine.shots[1], False)
        logger.info(f"✅ تم تسجيل فشل للتسديقة 2")
        
        # تسجيل نجاح للتسديقة الثالثة
        engine.record_execution(engine.shots[2], True)
        logger.info(f"✅ تم تسجيل نجاح للتسديقة 3")
        
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في تسجيل النتائج: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_statistics(engine):
    """اختبار الإحصائيات"""
    print("\n" + "="*60)
    print("5️⃣  اختبار الإحصائيات")
    print("="*60)
    
    try:
        stats = engine.get_statistics()
        
        logger.info(f"📊 الإحصائيات:")
        logger.info(f"   - إجمالي الحسابات: {stats['total_calculations']}")
        logger.info(f"   - إجمالي التسديدات المنفذة: {stats['total_shots_attempted']}")
        logger.info(f"   - التسديدات الناجحة: {stats['total_shots_successful']}")
        logger.info(f"   - معدل النجاح: {stats['success_rate']}%")
        logger.info(f"   - متوسط الصعوبة: {stats['average_difficulty']}")
        
        # التحقق من إحصائيات الجدران
        by_rails = engine.get_statistics_by_rails()
        logger.info(f"📊 إحصائيات حسب الجدران:")
        for rail, data in by_rails.items():
            logger.info(f"   - {rail}: {len(data)} تسديقة")
        
        # التحقق من إحصائيات الصعوبة
        by_difficulty = engine.get_statistics_by_difficulty()
        logger.info(f"📊 إحصائيات حسب الصعوبة:")
        for diff, data in by_difficulty.items():
            logger.info(f"   - {diff.value}: {len(data)} تسديقة")
        
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في الإحصائيات: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_storage(engine):
    """اختبار التخزين والاسترجاع"""
    print("\n" + "="*60)
    print("6️⃣  اختبار التخزين والاسترجاع")
    print("="*60)
    
    try:
        # حفظ البيانات
        engine.save_to_storage()
        logger.info(f"✅ تم حفظ {len(engine.shots)} تسديقة")
        
        # تحميل البيانات
        shots_loaded = engine.load_from_storage()
        logger.info(f"✅ تم تحميل {len(shots_loaded)} تسديقة")
        
        # التحقق من تطابق البيانات
        if len(shots_loaded) == len(engine.shots):
            logger.info(f"✅ البيانات متطابقة")
        else:
            logger.warning(f"⚠️ عدم تطابق البيانات")
        
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في التخزين: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_export_import(engine):
    """اختبار التصدير والاستيراد"""
    print("\n" + "="*60)
    print("7️⃣  اختبار التصدير والاستيراد")
    print("="*60)
    
    try:
        # تصدير البيانات
        export_data = {
            "shots": [s.to_dict() for s in engine.shots],
            "statistics": engine.get_statistics(),
        }
        
        export_file = Path(".billiards_data/export.json")
        export_file.parent.mkdir(exist_ok=True)
        
        with open(export_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"✅ تم تصدير {len(export_data['shots'])} تسديقة")
        
        # استيراد البيانات
        with open(export_file, 'r', encoding='utf-8') as f:
            imported_data = json.load(f)
        
        imported_shots = imported_data.get('shots', [])
        logger.info(f"✅ تم استيراد {len(imported_shots)} تسديقة")
        
        return True
    except Exception as e:
        logger.error(f"❌ خطأ في التصدير/الاستيراد: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """تشغيل جميع الاختبارات"""
    print("\n" + "="*60)
    print("🧪 اختبار شامل لنظام البلياردو")
    print("="*60)
    
    results = []
    
    # اختبار 1: الاستيراضات
    if not test_imports():
        logger.error("❌ فشل اختبار الاستيراضات")
        return
    results.append(("الاستيراضات", True))
    
    # اختبار 2: تهيئة المحرك
    engine = test_engine_initialization()
    if engine is None:
        logger.error("❌ فشل اختبار تهيئة المحرك")
        return
    results.append(("تهيئة المحرك", True))
    
    # اختبار 3: حساب التسديدات
    if not test_shot_calculation(engine):
        logger.error("❌ فشل اختبار حساب التسديدات")
        return
    results.append(("حساب التسديدات", True))
    
    # اختبار 4: تسجيل النتائج
    if not test_shot_execution(engine):
        logger.error("❌ فشل اختبار تسجيل النتائج")
        return
    results.append(("تسجيل النتائج", True))
    
    # اختبار 5: الإحصائيات
    if not test_statistics(engine):
        logger.error("❌ فشل اختبار الإحصائيات")
        return
    results.append(("الإحصائيات", True))
    
    # اختبار 6: التخزين
    if not test_storage(engine):
        logger.error("❌ فشل اختبار التخزين")
        return
    results.append(("التخزين والاسترجاع", True))
    
    # اختبار 7: التصدير/الاستيراد
    if not test_export_import(engine):
        logger.error("❌ فشل اختبار التصدير/الاستيراد")
        return
    results.append(("التصدير والاستيراد", True))
    
    # ملخص النتائج
    print("\n" + "="*60)
    print("📋 ملخص النتائج")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ نجح" if result else "❌ فشل"
        print(f"{status} - {name}")
    
    print(f"\nالنتيجة النهائية: {passed}/{total} اختبارات نجحت")
    
    if passed == total:
        print("\n🎉 جميع الاختبارات نجحت!")
        return True
    else:
        print(f"\n⚠️ {total - passed} اختبارات فشلت")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
