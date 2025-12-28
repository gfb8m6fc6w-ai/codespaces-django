"""
حاسبة التسديقات المحسّنة

يوفر فئة ShotCalculator لحساب جميع معاملات التسديقة
بما في ذلك الصعوبة والقوة والزاوية والنجاح المتوقع
"""

from typing import Optional, Dict
import logging
import sys
from pathlib import Path

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from backend.models.shot import Shot, Difficulty
    from backend.billiards.rail_system import RailPositionsSystem
except ImportError:
    from ..models.shot import Shot, Difficulty
    from .rail_system import RailPositionsSystem

logger = logging.getLogger(__name__)


class ShotCalculator:
    """
    حساب معاملات التسديقة والصعوبة والقوة والزاوية
    """
    
    def __init__(self):
        """تهيئة حاسبة التسديقات"""
        self.rail_system = RailPositionsSystem()
    
    def calculate_cue(self, target: float, white_ball: float) -> float:
        """
        حساب قيمة العصا
        الصيغة: Cue = Target + White Ball
        
        Args:
            target: قيمة الهدف (0-10)
            white_ball: قيمة الكرة البيضاء (0-10)
        
        Returns:
            قيمة العصا المحسوبة
        
        Raises:
            ValueError: إذا كانت القيم خارج النطاق المسموح
        """
        if not (0 <= target <= 10) or not (0 <= white_ball <= 10):
            raise ValueError("القيم يجب أن تكون بين 0 و 10")
        
        cue = target + white_ball
        return round(cue, 1)
    
    def calculate_difficulty(self, rails: int, target_distance: float, 
                           white_ball_distance: float) -> Difficulty:
        """
        حساب مستوى الصعوبة بناءً على عدد الجدران والمسافات
        
        صيغة الحساب:
        - الصعوبة الأساسية = 30
        - إضافة (rails - 1) * 20 بناءً على الجدران
        - إضافة المسافة النسبية
        
        Args:
            rails: عدد الجدران (1-4)
            target_distance: مسافة الهدف (0-10)
            white_ball_distance: مسافة الكرة البيضاء (0-10)
        
        Returns:
            مستوى الصعوبة (EASY, MEDIUM, HARD, VERY_HARD, EXTREME)
        
        Raises:
            ValueError: إذا كانت المدخلات غير صحيحة
        """
        if not (1 <= rails <= 4):
            raise ValueError("عدد الجدران يجب أن يكون بين 1 و 4")
        if not (0 <= target_distance <= 10) or not (0 <= white_ball_distance <= 10):
            raise ValueError("المسافات يجب أن تكون بين 0 و 10")
        
        base_difficulty = 30
        difficulty_score = base_difficulty + (rails - 1) * 20
        
        # إضافة الصعوبة بناءً على المسافة
        max_distance = 10.0
        distance_factor = (max(target_distance, white_ball_distance) / max_distance) * 30
        difficulty_score += distance_factor
        
        # تحديد مستوى الصعوبة
        if difficulty_score < 50:
            return Difficulty.EASY
        elif difficulty_score < 70:
            return Difficulty.MEDIUM
        elif difficulty_score < 85:
            return Difficulty.HARD
        elif difficulty_score < 100:
            return Difficulty.VERY_HARD
        else:
            return Difficulty.EXTREME
    
    def calculate_success_rate(self, rails: int, difficulty: Difficulty) -> float:
        """
        حساب معدل النجاح المتوقع
        
        Args:
            rails: عدد الجدران (1-4)
            difficulty: مستوى الصعوبة
        
        Returns:
            معدل النجاح (0-100)
        
        Raises:
            ValueError: إذا كانت المدخلات غير صحيحة
        """
        if not (1 <= rails <= 4):
            raise ValueError("عدد الجدران يجب أن يكون بين 1 و 4")
        
        # معدل النجاح الأساسي حسب الصعوبة
        base_rates = {
            Difficulty.EASY: 90.0,
            Difficulty.MEDIUM: 70.0,
            Difficulty.HARD: 50.0,
            Difficulty.VERY_HARD: 30.0,
            Difficulty.EXTREME: 10.0,
        }
        
        rate = base_rates.get(difficulty, 50.0)
        
        # تقليل المعدل بناءً على عدد الجدران
        rails_penalty = (rails - 1) * 5.0
        rate = max(5.0, rate - rails_penalty)
        
        return float(rate)
    
    def calculate_power_required(self, rails: int, white_ball: float, 
                                target: float) -> float:
        """
        حساب القوة المطلوبة للتسديقة
        
        صيغة الحساب:
        power = 50 + (white_ball * 2) + (target * 1.5)
        power *= (1 + (rails - 1) * 0.2)
        
        Args:
            rails: عدد الجدران (1-4)
            white_ball: قيمة الكرة البيضاء (0-10)
            target: قيمة الهدف (0-10)
        
        Returns:
            القوة المطلوبة (10-100)
        
        Raises:
            ValueError: إذا كانت المدخلات غير صحيحة
        """
        if not (0 <= white_ball <= 10) or not (0 <= target <= 10):
            raise ValueError("القيم يجب أن تكون بين 0 و 10")
        
        power = 50 + (white_ball * 2) + (target * 1.5)
        power *= (1 + (rails - 1) * 0.2)
        
        return min(100.0, max(10.0, power))
    
    def calculate_angle_required(self, cue: float, white_ball: float) -> float:
        """
        حساب الزاوية المطلوبة
        
        Args:
            cue: قيمة العصا (0-20)
            white_ball: قيمة الكرة البيضاء (0-10)
        
        Returns:
            الزاوية بالدرجات (0-180)
        """
        angle = (cue * 9) % 180  # 180 درجة كأقصى زاوية
        return float(angle)
    
    def create_shot(self, rails: int, cue_position: float, white_ball: float,
                   target: float, pocket: int) -> Shot:
        """
        إنشاء تسديقة محسوبة كاملة
        
        Args:
            rails: عدد الجدران (1-4)
            cue_position: موضع العصا (0-10)
            white_ball: موضع الكرة البيضاء (0-10)
            target: موضع الهدف (0-10)
            pocket: موضع الجيب (0-5)
        
        Returns:
            كائن Shot محسوب بجميع المعاملات
        
        Raises:
            ValueError: إذا كانت المدخلات غير صحيحة
        """
        try:
            cue = self.calculate_cue(target, white_ball)
            difficulty = self.calculate_difficulty(rails, target, white_ball)
            success_rate = self.calculate_success_rate(rails, difficulty)
            
            shot = Shot(
                rails=rails,
                cue_position=cue_position,
                white_ball=white_ball,
                target=target,
                pocket=pocket,
                difficulty=difficulty,
                success_rate=success_rate,
            )
            
            logger.info(f"✅ تسديقة محسوبة: {rails} جدران، صعوبة {difficulty.value}")
            return shot
            
        except ValueError as e:
            logger.error(f"❌ خطأ في حساب التسديقة: {e}")
            raise
    
    def get_calculation_summary(self, shot: Shot) -> dict:
        """
        الحصول على ملخص حسابات التسديقة
        
        Args:
            shot: كائن التسديقة
        
        Returns:
            قاموس يحتوي على جميع الحسابات
        """
        try:
            cue = self.calculate_cue(shot.target, shot.white_ball)
            power = self.calculate_power_required(shot.rails, shot.white_ball, shot.target)
            angle = self.calculate_angle_required(cue, shot.white_ball)
            
            return {
                'cue_value': cue,
                'power_required': round(power, 1),
                'angle_required': round(angle, 1),
                'difficulty': shot.difficulty.value,
                'success_rate': round(shot.success_rate, 1),
                'rails': shot.rails,
                'pocket': shot.pocket,
            }
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء الملخص: {e}")
            raise
