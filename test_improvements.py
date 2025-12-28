"""
اختبارات شاملة لنظام البلياردو المحسّن
مع حالات اختبار لمعالجة الأخطاء والأداء
"""

import pytest
import sys
from pathlib import Path
import logging

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent.parent))

from billiards.engine import BilliardsEngine
from billiards.calculator import ShotCalculator
from billiards.rail_system import RailPositionsSystem
from models.shot import Shot, Difficulty, ShotResult


# إعداد Logging للاختبارات
logging.basicConfig(level=logging.WARNING)


class TestRailPositionsSystem:
    """اختبارات نظام الجدران"""
    
    @pytest.fixture
    def rail_system(self):
        return RailPositionsSystem()
    
    def test_valid_angle_calculation(self, rail_system):
        """اختبار حساب الزاوية الصحيح"""
        angle = rail_system.get_angle_for_rails(1, 5.0)
        assert angle == 90.0, "الزاوية يجب أن تكون 90 درجة للموضع 5"
    
    def test_invalid_rails_count(self, rail_system):
        """اختبار معالجة عدد جدران غير صحيح"""
        with pytest.raises(ValueError):
            rail_system.get_angle_for_rails(5, 5.0)
        
        with pytest.raises(ValueError):
            rail_system.get_angle_for_rails(0, 5.0)
    
    def test_invalid_position(self, rail_system):
        """اختبار معالجة موضع غير صحيح"""
        with pytest.raises(ValueError):
            rail_system.get_angle_for_rails(1, 15.0)
        
        with pytest.raises(ValueError):
            rail_system.get_angle_for_rails(1, -1.0)
    
    def test_angle_interpolation(self, rail_system):
        """اختبار الاستيفاء الزاوي"""
        # بين 90 و 108 درجة للموضع بين 5 و 6
        angle = rail_system.get_angle_for_rails(1, 5.5)
        assert 90 < angle < 108, "الزاوية يجب أن تكون بين 90 و 108"
    
    def test_cache_performance(self, rail_system):
        """اختبار كفاءة الذاكرة المؤقتة"""
        # الحصول على نفس الزاوية مرتين
        angle1 = rail_system.get_angle_for_rails(1, 5.0)
        angle2 = rail_system.get_angle_for_rails(1, 5.0)
        
        assert angle1 == angle2, "النتائج يجب أن تكون متطابقة"
        assert rail_system.get_angle_for_rails.cache_info().hits > 0, "الذاكرة يجب أن تعمل"
    
    def test_custom_position(self, rail_system):
        """اختبار إضافة موضع مخصص"""
        rail_system.add_custom_position(1, 7.5, 135.0, "موضع خاص")
        angle = rail_system.get_angle_for_rails(1, 7.5)
        assert angle == 135.0, "الموضع المخصص يجب أن يعمل"
    
    def test_distance_calculation(self, rail_system):
        """اختبار حساب المسافة بين موضعين"""
        distance = rail_system.get_distance_between_positions(1, 0, 5)
        assert distance == 90, "المسافة من 0 إلى 5 يجب أن تكون 90 درجة"
    
    def test_cache_stats(self, rail_system):
        """اختبار إحصائيات الذاكرة"""
        rail_system.get_angle_for_rails(1, 5.0)
        stats = rail_system.get_cache_stats()
        assert "interpolation_cache_size" in stats, "يجب تضمين حجم الذاكرة"


class TestShotCalculator:
    """اختبارات حاسبة التسديقات"""
    
    @pytest.fixture
    def calculator(self):
        return ShotCalculator()
    
    def test_valid_cue_calculation(self, calculator):
        """اختبار حساب قيمة العصا"""
        cue = calculator.calculate_cue(target=3.0, white_ball=5.0)
        assert cue == 8.0, "قيمة العصا يجب أن تكون 8.0"
    
    def test_invalid_rails(self, calculator):
        """اختبار معالجة عدد جدران غير صحيح"""
        with pytest.raises(ValueError):
            calculator.calculate_difficulty(rails=0)
        
        with pytest.raises(ValueError):
            calculator.calculate_difficulty(rails=5)
    
    def test_negative_position(self, calculator):
        """اختبار معالجة الأرقام السالبة"""
        with pytest.raises(ValueError):
            calculator.calculate_cue(target=-1, white_ball=5)
    
    def test_out_of_bounds_position(self, calculator):
        """اختبار معالجة الأرقام خارج الحدود"""
        with pytest.raises(ValueError):
            calculator.calculate_cue(target=15, white_ball=5)
    
    def test_difficulty_caching(self, calculator):
        """اختبار caching صعوبة التسديقة"""
        difficulty1 = calculator.calculate_difficulty(rails=1)
        difficulty2 = calculator.calculate_difficulty(rails=1)
        
        assert difficulty1 == difficulty2, "النتائج يجب أن تكون متطابقة"
        # التحقق من استخدام الذاكرة
        assert len(calculator._difficulty_cache) > 0, "الذاكرة يجب أن تحتوي على قيم"
    
    def test_success_rate_range(self, calculator):
        """اختبار أن معدل النجاح في النطاق الصحيح"""
        rate = calculator.calculate_success_rate(rails=1, difficulty=Difficulty.EASY)
        assert 0 <= rate <= 1, "معدل النجاح يجب أن يكون بين 0 و 1"
    
    def test_power_calculation(self, calculator):
        """اختبار حساب القوة"""
        power = calculator.calculate_power_required(rails=1, pocket=0)
        assert 0 < power <= 100, "القوة يجب أن تكون بين 0 و 100"
    
    def test_angle_bounds(self, calculator):
        """اختبار حدود الزاوية"""
        angle = calculator.calculate_angle_required(rails=1, cue_position=5)
        assert 0 <= angle <= 360, "الزاوية يجب أن تكون بين 0 و 360"
    
    def test_clear_cache(self, calculator):
        """اختبار مسح الذاكرة المؤقتة"""
        calculator.calculate_difficulty(rails=1)
        assert len(calculator._difficulty_cache) > 0, "الذاكرة يجب أن تحتوي على قيم"
        
        calculator.clear_cache()
        assert len(calculator._difficulty_cache) == 0, "الذاكرة يجب أن تكون فارغة"


class TestBilliardsEngine:
    """اختبارات محرك البلياردو"""
    
    @pytest.fixture
    def engine(self):
        return BilliardsEngine()
    
    def test_valid_shot_creation(self, engine):
        """اختبار إنشاء تسديقة صحيحة"""
        shot = engine.calculate_shot(rails=1, cue_position=2.0, 
                                     white_ball=5.0, target=3.0, pocket=0)
        
        assert isinstance(shot, Shot), "يجب أن ترجع Shot"
        assert shot.rails == 1, "عدد الجدران يجب أن يكون 1"
    
    def test_invalid_rails_range(self, engine):
        """اختبار معالجة عدد جدران خارج النطاق"""
        with pytest.raises(ValueError):
            engine.calculate_shot(rails=0, cue_position=2.0, 
                                 white_ball=5.0, target=3.0, pocket=0)
    
    def test_invalid_pocket_range(self, engine):
        """اختبار معالجة رقم جيب غير صحيح"""
        with pytest.raises(ValueError):
            engine.calculate_shot(rails=1, cue_position=2.0, 
                                 white_ball=5.0, target=3.0, pocket=6)
    
    def test_record_execution(self, engine):
        """اختبار تسجيل نتيجة التسديقة"""
        shot = engine.calculate_shot(rails=1, cue_position=2.0, 
                                     white_ball=5.0, target=3.0, pocket=0)
        
        engine.record_execution(shot, True)
        
        assert shot.executed, "التسديقة يجب أن تكون منفذة"
        assert shot.result, "النتيجة يجب أن تكون ناجحة"
    
    def test_get_shots_by_rails(self, engine):
        """اختبار استرجاع التسديقات حسب الجدران"""
        # إضافة تسديقات مختلفة
        shot1 = engine.calculate_shot(rails=1, cue_position=2.0, 
                                      white_ball=5.0, target=3.0, pocket=0)
        shot2 = engine.calculate_shot(rails=2, cue_position=2.0, 
                                      white_ball=5.0, target=3.0, pocket=0)
        
        shots_1_rail = engine.get_shots_by_rails(1)
        shots_2_rail = engine.get_shots_by_rails(2)
        
        assert any(s.rails == 1 for s in shots_1_rail), "يجب أن تحتوي على تسديقات جدار واحد"
        assert any(s.rails == 2 for s in shots_2_rail), "يجب أن تحتوي على تسديقات جدارين"
    
    def test_get_shots_by_difficulty(self, engine):
        """اختبار استرجاع التسديقات حسب الصعوبة"""
        shot = engine.calculate_shot(rails=1, cue_position=2.0, 
                                     white_ball=5.0, target=3.0, pocket=0)
        
        easy_shots = engine.get_shots_by_difficulty(Difficulty.EASY)
        assert len(easy_shots) > 0, "يجب أن تحتوي على تسديقات سهلة"
    
    def test_performance_stats(self, engine):
        """اختبار الحصول على إحصائيات الأداء"""
        engine.calculate_shot(rails=1, cue_position=2.0, 
                             white_ball=5.0, target=3.0, pocket=0)
        
        stats = engine.get_performance_stats()
        assert "total_shots" in stats, "يجب تضمين عدد التسديقات"
        assert "total_calculations" in stats, "يجب تضمين الحسابات"
    
    def test_statistics(self, engine):
        """اختبار الحصول على الإحصائيات"""
        engine.calculate_shot(rails=1, cue_position=2.0, 
                             white_ball=5.0, target=3.0, pocket=0)
        
        stats = engine.get_statistics()
        assert stats is not None, "يجب أن تعيد الإحصائيات"
    
    def test_clear_old_data(self, engine):
        """اختبار حذف البيانات القديمة"""
        initial_count = len(engine.shots)
        deleted = engine.clear_old_data(days=-1)  # حذف جميع البيانات
        
        assert deleted >= 0, "يجب أن ترجع عدد الحذوفات"
    
    def test_storage_operations(self, engine):
        """اختبار عمليات التخزين"""
        engine.calculate_shot(rails=1, cue_position=2.0, 
                             white_ball=5.0, target=3.0, pocket=0)
        
        # حفظ البيانات
        engine.save_to_storage()
        
        # تحميل البيانات
        engine.load_from_storage()
        
        assert len(engine.shots) > 0, "يجب أن تحتوي على بيانات بعد التحميل"


class TestEdgeCases:
    """اختبارات الحالات الحدية"""
    
    def test_boundary_values(self):
        """اختبار القيم الحدية"""
        calculator = ShotCalculator()
        
        # الحد الأدنى
        cue_min = calculator.calculate_cue(0, 0)
        assert cue_min == 0, "الحد الأدنى يجب أن يكون 0"
        
        # الحد الأقصى
        cue_max = calculator.calculate_cue(10, 10)
        assert cue_max == 20, "الحد الأقصى يجب أن يكون 20"
    
    def test_floating_point_precision(self):
        """اختبار دقة الفاصلة العائمة"""
        rail_system = RailPositionsSystem()
        
        # اختبار الأرقام العشرية الدقيقة
        angle = rail_system.get_angle_for_rails(1, 5.333)
        assert isinstance(angle, float), "يجب أن ترجع float"
    
    def test_concurrent_calculations(self):
        """اختبار الحسابات المتزامنة"""
        calculator = ShotCalculator()
        
        # حساب متعدد في نفس الوقت
        results = []
        for i in range(10):
            cue = calculator.calculate_cue(i, i+1)
            results.append(cue)
        
        assert len(results) == 10, "يجب أن ننجز جميع الحسابات"
    
    def test_memory_cleanup(self):
        """اختبار تنظيف الذاكرة"""
        calculator = ShotCalculator()
        rail_system = RailPositionsSystem()
        
        # إنشاء بيانات كثيرة
        for i in range(100):
            calculator.calculate_difficulty(rails=(i % 4) + 1)
        
        # تنظيف الذاكرة
        calculator.clear_cache()
        rail_system.clear_interpolation_cache()
        
        # التحقق من التنظيف
        assert len(calculator._difficulty_cache) == 0, "يجب أن تكون الذاكرة فارغة"


# اختبارات الأداء
class TestPerformance:
    """اختبارات الأداء والسرعة"""
    
    def test_calculation_speed(self):
        """اختبار سرعة الحساب"""
        calculator = ShotCalculator()
        
        import time
        start = time.time()
        
        for _ in range(1000):
            calculator.calculate_cue(5.0, 5.0)
        
        elapsed = time.time() - start
        
        # يجب أن تكون سريعة جداً مع caching
        assert elapsed < 0.1, f"الحسابات بطيئة جداً: {elapsed}s"
    
    def test_cache_efficiency(self):
        """اختبار كفاءة الذاكرة"""
        calculator = ShotCalculator()
        
        # اختبار بدون ذاكرة
        for _ in range(100):
            calculator.calculate_difficulty(rails=1)
        
        cache_info = calculator.calculate_cue.cache_info()
        assert cache_info.hits > 0, "الذاكرة يجب أن توفر تسريعاً"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
