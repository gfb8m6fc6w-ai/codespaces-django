"""
حاسبة التسديقات - محسّنة بـ Caching والأداء
"""

from typing import Optional, Dict
from ..models.shot import Shot, Difficulty
from .rail_system import RailPositionsSystem
import math
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


class ShotCalculator:
    """
    حاسبة التسديقات المتقدمة
    مع دعم caching وتحسينات الأداء
    """
    
    def __init__(self):
        self.rail_system = RailPositionsSystem()
        self._difficulty_cache: Dict[tuple, Difficulty] = {}
        self._success_rate_cache: Dict[tuple, float] = {}
    
    @lru_cache(maxsize=512)
    def calculate_cue(self, target: float, white_ball: float) -> float:
        """
        حساب قيمة العصا
        الصيغة: Cue = Target + White Ball
        
        Args:
            target: قيمة الهدف
            white_ball: قيمة الكرة البيضاء
        
        Returns:
            قيمة العصا المحسوبة
        """
        try:
            if not (0 <= target <= 10 and 0 <= white_ball <= 10):
                raise ValueError("القيم يجب أن تكون بين 0 و 10")
            
            cue = target + white_ball
            return round(cue, 1)
        except Exception as e:
            logger.error(f"خطأ في حساب العصا: {e}")
            raise
    
    def calculate_difficulty(self, rails: int, target_distance: float, 
                           white_ball_distance: float) -> Difficulty:
        """
        حساب مستوى الصعوبة بناءً على عدد الجدران والمسافات
        مع caching للنتائج
        
        Args:
            rails: عدد الجدران (1-4)
            target_distance: مسافة الهدف
            white_ball_distance: مسافة الكرة البيضاء
        
        Returns:
            مستوى الصعوبة
        """
        # التحقق من الـ cache أولاً
        cache_key = (rails, round(target_distance, 2), round(white_ball_distance, 2))
        if cache_key in self._difficulty_cache:
            return self._difficulty_cache[cache_key]
        
        try:
            if not (1 <= rails <= 4):
                raise ValueError("عدد الجدران يجب أن يكون بين 1 و 4")
            
            base_difficulty = 30
            
            # إضافة الصعوبة بناءً على عدد الجدران
            difficulty_score = base_difficulty + (rails - 1) * 20
            
            # إضافة الصعوبة بناءً على المسافة
            max_distance = 8.0
            distance_factor = (max(target_distance, white_ball_distance) / max_distance) * 20
            difficulty_score += distance_factor
            
            # تحديد مستوى الصعوبة
            if difficulty_score < 40:
                result = Difficulty.EASY
            elif difficulty_score < 60:
                result = Difficulty.MEDIUM
            elif difficulty_score < 80:
                result = Difficulty.HARD
            elif difficulty_score < 100:
                result = Difficulty.VERY_HARD
            else:
                result = Difficulty.EXTREME
            
            # حفظ في الـ cache
            self._difficulty_cache[cache_key] = result
            return result
        
        except Exception as e:
            logger.error(f"خطأ في حساب الصعوبة: {e}")
            raise
    
    def calculate_success_rate(self, rails: int, difficulty: Difficulty) -> float:
        """
        حساب معدل النجاح المتوقع
        مع caching للنتائج
        
        Args:
            rails: عدد الجدران
            difficulty: مستوى الصعوبة
        
        Returns:
            معدل النجاح (0-100)
        """
        # التحقق من الـ cache
        cache_key = (rails, difficulty.value)
        if cache_key in self._success_rate_cache:
            return self._success_rate_cache[cache_key]
        
        try:
            if not (1 <= rails <= 4):
                raise ValueError("عدد الجدران غير صحيح")
            
            # معدل النجاح الأساسي
            base_rates = {
                Difficulty.EASY: 90,
                Difficulty.MEDIUM: 70,
                Difficulty.HARD: 50,
                Difficulty.VERY_HARD: 30,
                Difficulty.EXTREME: 10,
            }
            
            rate = base_rates.get(difficulty, 50)
            
            # تقليل المعدل بناءً على عدد الجدران
            rails_penalty = (rails - 1) * 5
            rate = max(5, rate - rails_penalty)
            
            # حفظ في الـ cache
            self._success_rate_cache[cache_key] = float(rate)
            return float(rate)
        
        except Exception as e:
            logger.error(f"خطأ في حساب معدل النجاح: {e}")
            raise
    
    def calculate_power_required(self, rails: int, white_ball: float, 
                                target: float) -> float:
        """
        حساب القوة المطلوبة للتسديقة
        محسّنة لتقليل الحسابات غير الضرورية
        
        Args:
            rails: عدد الجدران
            white_ball: قيمة الكرة البيضاء
            target: قيمة الهدف
        
        Returns:
            القوة المطلوبة (0-100)
        """
        try:
            if not (1 <= rails <= 4):
                raise ValueError("عدد الجدران غير صحيح")
            if not (0 <= white_ball <= 10 and 0 <= target <= 10):
                raise ValueError("القيم يجب أن تكون بين 0 و 10")
            
            # حساب محسّن
            base_power = 50
            white_ball_factor = white_ball * 2
            target_factor = target * 1.5
            
            power = base_power + white_ball_factor + target_factor
            
            # تطبيق مضاعف الجدران
            rails_multiplier = 1 + (rails - 1) * 0.2
            power *= rails_multiplier
            
            # تقييد النتيجة بكفاءة
            return min(100.0, max(10.0, power))
        
        except Exception as e:
            logger.error(f"خطأ في حساب القوة: {e}")
            raise
    
    def calculate_angle_required(self, cue: float, white_ball: float) -> float:
        """
        حساب الزاوية المطلوبة
        
        Args:
            cue: قيمة العصا
            white_ball: قيمة الكرة البيضاء
        
        Returns:
            الزاوية بالدرجات
        """
        try:
            if not (0 <= cue <= 20):
                raise ValueError("قيمة العصا خارج النطاق")
            
            # تحويل القيم إلى زاوية
            angle = (cue * 18) % 180
            return float(angle)
        
        except Exception as e:
            logger.error(f"خطأ في حساب الزاوية: {e}")
            raise
    
    def create_shot(self, rails: int, cue_position: float, white_ball: float,
                   target: float, pocket: int) -> Shot:
        """
        إنشاء تسديقة محسوبة كاملة
        
        Args:
            rails: عدد الجدران
            cue_position: موضع العصا
            white_ball: موضع الكرة البيضاء
            target: موضع الهدف
            pocket: موضع الجيب
        
        Returns:
            كائن التسديقة المحسوب
        """
        try:
            # التحقق المبكر من الصحة
            if not (1 <= rails <= 4):
                raise ValueError(f"عدد الجدران يجب أن يكون بين 1 و 4")
            
            cue = self.calculate_cue(target, white_ball)
            difficulty = self.calculate_difficulty(rails, target, white_ball)
            success_rate = self.calculate_success_rate(rails, difficulty)
            
            return Shot(
                rails=rails,
                cue_position=cue_position,
                white_ball=white_ball,
                target=target,
                pocket=pocket,
                difficulty=difficulty,
                success_rate=success_rate,
            )
        
        except Exception as e:
            logger.error(f"خطأ في إنشاء التسديقة: {e}")
            raise
    
    def get_calculation_summary(self, shot: Shot) -> dict:
        """
        الحصول على ملخص حسابات التسديقة
        
        Args:
            shot: التسديقة
        
        Returns:
            قاموس بالحسابات
        """
        try:
            cue = self.calculate_cue(shot.target, shot.white_ball)
            power = self.calculate_power_required(shot.rails, shot.white_ball, shot.target)
            angle = self.calculate_angle_required(cue, shot.white_ball)
            
            return {
                'cue_value': cue,
                'power_required': power,
                'angle_required': angle,
                'difficulty': shot.difficulty.value,
                'success_rate': shot.success_rate,
                'rails': shot.rails,
                'pocket': shot.pocket,
            }
        
        except Exception as e:
            logger.error(f"خطأ في الحصول على ملخص الحسابات: {e}")
            raise
    
    def clear_cache(self) -> None:
        """مسح الـ cache لتحرير الذاكرة"""
        self._difficulty_cache.clear()
        self._success_rate_cache.clear()
        logger.info("تم مسح الـ cache")
