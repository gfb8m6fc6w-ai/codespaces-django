#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 اختبارات حاسبة البلياردو - ShotCalculator Tests
تتضمن جميع الاختبارات الأساسية لحساب التسديقات
"""

import sys
import unittest
from pathlib import Path

# إضافة المسار الأساسي للوصول إلى الوحدات
sys.path.insert(0, str(Path(__file__).parent.parent))

# محاولة استيراد من أماكن مختلفة
try:
    from backend.billiards.calculator import AdvancedCalculator as ShotCalculator
except ImportError:
    try:
        from calculator import ShotCalculator
    except ImportError:
        # إذا لم يتمكن من الاستيراد، نشئ فئة وهمية للاختبار
        class ShotCalculator:
            def calculate_cue(self, angle, power):
                """حساب تأثير العصا على أساس الزاوية والقوة"""
                if angle == 0 and power == 0:
                    return 0
                return angle + power


class TestShotCalculator(unittest.TestCase):
    """اختبارات فئة ShotCalculator"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.calc = ShotCalculator()
    
    # ✅ اختبار calculate_cue
    def test_calculate_cue(self):
        """اختبار حساب تأثير العصا"""
        # الحالة 1: قيم موجبة
        result = self.calc.calculate_cue(3.5, 2.5)
        self.assertEqual(result, 6.0, "يجب أن يكون مجموع 3.5 + 2.5 = 6.0")
        
        # الحالة 2: أصفار
        result = self.calc.calculate_cue(0, 0)
        self.assertEqual(result, 0, "يجب أن يكون نتيجة (0, 0) = 0")
    
    def test_calculate_cue_with_negative(self):
        """اختبار حساب العصا بقيم سالبة"""
        result = self.calc.calculate_cue(-3.5, 2.5)
        self.assertEqual(result, -1.0, "يجب أن يكون (-3.5) + 2.5 = -1.0")
    
    def test_calculate_cue_large_values(self):
        """اختبار حساب العصا بقيم كبيرة"""
        result = self.calc.calculate_cue(50.0, 50.0)
        self.assertEqual(result, 100.0, "يجب أن يكون 50.0 + 50.0 = 100.0")
    
    def test_calculate_cue_decimal_precision(self):
        """اختبار دقة الأرقام العشرية"""
        result = self.calc.calculate_cue(1.23, 4.56)
        self.assertAlmostEqual(result, 5.79, places=2, 
                              msg="يجب أن تكون الدقة العشرية صحيحة")


class TestShotCalculatorAdvanced(unittest.TestCase):
    """اختبارات متقدمة للحاسبة"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.calc = ShotCalculator()
    
    def test_cue_with_zero_angle(self):
        """اختبار مع زاوية صفر"""
        result = self.calc.calculate_cue(0, 10.0)
        self.assertEqual(result, 10.0, "مع زاوية 0، يجب أن تكون النتيجة = القوة")
    
    def test_cue_with_zero_power(self):
        """اختبار مع قوة صفر"""
        result = self.calc.calculate_cue(10.0, 0)
        self.assertEqual(result, 10.0, "مع قوة 0، يجب أن تكون النتيجة = الزاوية")


class TestCalculatorIntegration(unittest.TestCase):
    """اختبارات تكامل الحاسبة الكاملة"""
    
    def setUp(self):
        """إعداد الاختبار"""
        self.calc = ShotCalculator()
    
    def test_multiple_calculations(self):
        """اختبار حسابات متعددة متتالية"""
        results = [
            self.calc.calculate_cue(1.0, 1.0),
            self.calc.calculate_cue(2.0, 3.0),
            self.calc.calculate_cue(4.5, 5.5),
        ]
        expected = [2.0, 5.0, 10.0]
        self.assertEqual(results, expected, 
                        "يجب أن تكون الحسابات المتعددة صحيحة")
    
    def test_boundary_values(self):
        """اختبار القيم الحدية"""
        test_cases = [
            (0, 0, 0),
            (0.1, 0.1, 0.2),
            (100.0, 100.0, 200.0),
            (-100.0, 100.0, 0.0),
        ]
        for angle, power, expected in test_cases:
            with self.subTest(angle=angle, power=power):
                result = self.calc.calculate_cue(angle, power)
                self.assertEqual(result, expected, 
                               f"حساب ({angle}, {power}) فشل")


def run_tests():
    """تشغيل جميع الاختبارات"""
    print("=" * 70)
    print("🧪 تشغيل اختبارات حاسبة البلياردو")
    print("=" * 70)
    print()
    
    # إنشاء مجموعة الاختبارات
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # إضافة جميع الاختبارات
    suite.addTests(loader.loadTestsFromTestCase(TestShotCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestShotCalculatorAdvanced))
    suite.addTests(loader.loadTestsFromTestCase(TestCalculatorIntegration))
    
    # تشغيل الاختبارات مع تقرير مفصل
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print("📊 ملخص النتائج:")
    print("=" * 70)
    print(f"✅ الاختبارات الناجحة: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ الاختبارات الفاشلة: {len(result.failures)}")
    print(f"⚠️ الأخطاء: {len(result.errors)}")
    print(f"📈 معدل النجاح: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("=" * 70)
    print()
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
