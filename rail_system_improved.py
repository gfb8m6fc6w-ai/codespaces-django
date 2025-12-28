"""
نظام مواضع الجدران المحسّن مع caching وأداء محسّنة
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from functools import lru_cache
import math
import logging

# إعداد Logging
logger = logging.getLogger(__name__)


@dataclass
class RailPosition:
    """موضع على الجدار"""
    rail: int  # عدد الجدران (1-4)
    position: float  # موضع العصا (0-10)
    angle: float  # الزاوية بالدرجات
    description: str  # وصف الموضع


class RailPositionsSystem:
    """
    نظام مواضع الجدران المحسّن
    مع caching للاستيفاء والحسابات الزاويّة
    """
    
    # قاموس مواضع الجدران الافتراضي
    RAIL_POSITIONS: Dict[int, Dict[float, Tuple[float, str]]] = {
        1: {  # جدار واحد
            0.0: (0, "الجدار الأول - الزاوية اليسرى"),
            1.0: (18, "موضع 1"),
            2.0: (36, "موضع 2"),
            3.0: (54, "موضع 3"),
            4.0: (72, "موضع 4"),
            5.0: (90, "موضع 5 - الوسط"),
            6.0: (108, "موضع 6"),
            7.0: (126, "موضع 7"),
            8.0: (144, "موضع 8"),
            9.0: (162, "موضع 9"),
            10.0: (180, "الجدار الأول - الزاوية اليمنى"),
        },
        2: {  # جداران
            0.0: (0, "الجدار الأول والثاني - الزاوية"),
            2.5: (45, "موضع 2.5"),
            5.0: (90, "الوسط"),
            7.5: (135, "موضع 7.5"),
            10.0: (180, "الجدار الأول والثاني - الزاوية"),
        },
        3: {  # ثلاثة جدران
            0.0: (0, "الزاوية الأولى"),
            3.33: (60, "موضع متوسط"),
            6.67: (120, "موضع متوسط"),
            10.0: (180, "الزاوية الثانية"),
        },
        4: {  # أربعة جدران
            0.0: (0, "الزاوية الأولى"),
            2.5: (45, "موضع 2.5"),
            5.0: (90, "الوسط"),
            7.5: (135, "موضع 7.5"),
            10.0: (180, "الزاوية الثانية"),
        }
    }
    
    def __init__(self):
        """تهيئة نظام الجدران"""
        try:
            self.custom_positions: Dict[int, Dict[float, Tuple[float, str]]] = {}
            self._interpolation_cache: Dict[Tuple, float] = {}
            logger.info("✅ تم تهيئة نظام الجدران")
        except Exception as e:
            logger.error(f"❌ خطأ في تهيئة نظام الجدران: {e}")
            raise
    
    @lru_cache(maxsize=512)
    def get_angle_for_rails(self, rails: int, position: float) -> float:
        """
        الحصول على الزاوية لموضع معين مع caching
        
        Args:
            rails: عدد الجدران (1-4)
            position: الموضع (0-10)
        
        Returns:
            الزاوية بالدرجات
        """
        try:
            if not 1 <= rails <= 4:
                raise ValueError(f"عدد الجدران يجب أن يكون بين 1 و 4، الحالي: {rails}")
            
            if not 0 <= position <= 10:
                raise ValueError(f"الموضع يجب أن يكون بين 0 و 10، الحالي: {position}")
            
            # البحث في المواضع المخزنة
            positions_dict = self.RAIL_POSITIONS.get(rails, {})
            
            # إذا كان الموضع موجوداً مباشرة
            if position in positions_dict:
                angle, _ = positions_dict[position]
                logger.debug(f"✓ تم استرجاع الزاوية مباشرة: {rails} جدران، موضع {position} → {angle}°")
                return float(angle)
            
            # البحث بالاستيفاء
            angle = self._interpolate_angle(rails, position)
            logger.debug(f"✓ تم استيفاء الزاوية: {rails} جدران، موضع {position} → {angle}°")
            return angle
        
        except (ValueError, KeyError) as e:
            logger.error(f"❌ خطأ في حساب الزاوية: {e}")
            raise
    
    def _interpolate_angle(self, rails: int, position: float) -> float:
        """
        استيفاء الزاوية بين موضعين معروفين
        """
        # التحقق من الذاكرة المؤقتة أولاً
        cache_key = (rails, round(position, 2))
        if cache_key in self._interpolation_cache:
            return self._interpolation_cache[cache_key]
        
        positions_dict = self.RAIL_POSITIONS[rails]
        sorted_positions = sorted(positions_dict.keys())
        
        # البحث عن أقرب موضعين
        lower_pos = None
        upper_pos = None
        
        for i, pos in enumerate(sorted_positions):
            if pos <= position:
                lower_pos = pos
            if pos >= position and upper_pos is None:
                upper_pos = pos
        
        # إذا كان الموضع على الحدود
        if lower_pos is None:
            lower_pos = sorted_positions[0]
        if upper_pos is None:
            upper_pos = sorted_positions[-1]
        
        # إذا كان الموضع محدداً بدقة
        if lower_pos == upper_pos:
            angle = positions_dict[lower_pos][0]
        else:
            # حساب الاستيفاء الخطي
            lower_angle, _ = positions_dict[lower_pos]
            upper_angle, _ = positions_dict[upper_pos]
            
            # منع الالتفاف حول 360 درجة
            if abs(upper_angle - lower_angle) > 180:
                if upper_angle > lower_angle:
                    lower_angle += 360
                else:
                    upper_angle += 360
            
            ratio = (position - lower_pos) / (upper_pos - lower_pos)
            angle = lower_angle + (upper_angle - lower_angle) * ratio
            angle = angle % 360  # تحديد النطاق
        
        # حفظ في الذاكرة المؤقتة
        self._interpolation_cache[cache_key] = angle
        return angle
    
    def get_position_description(self, rails: int, position: float) -> str:
        """
        الحصول على وصف الموضع
        """
        try:
            positions_dict = self.RAIL_POSITIONS.get(rails, {})
            
            if position in positions_dict:
                _, description = positions_dict[position]
                return description
            
            return f"موضع مخصص - {rails} جدران، الموضع {position}"
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على وصف الموضع: {e}")
            return "موضع غير معروف"
    
    def get_rail_positions(self, rails: int) -> List[RailPosition]:
        """
        الحصول على جميع مواضع جدار معين
        """
        try:
            if not 1 <= rails <= 4:
                raise ValueError(f"عدد الجدران يجب أن يكون بين 1 و 4")
            
            positions_dict = self.RAIL_POSITIONS[rails]
            result = []
            
            for position, (angle, description) in positions_dict.items():
                result.append(RailPosition(
                    rail=rails,
                    position=position,
                    angle=angle,
                    description=description
                ))
            
            logger.info(f"✓ تم استرجاع {len(result)} موضع للجدران {rails}")
            return sorted(result, key=lambda x: x.position)
        
        except Exception as e:
            logger.error(f"❌ خطأ في استرجاع مواضع الجدران: {e}")
            raise
    
    def add_custom_position(self, rails: int, position: float, angle: float, 
                          description: str = "موضع مخصص"):
        """
        إضافة موضع مخصص
        """
        try:
            if not 1 <= rails <= 4:
                raise ValueError(f"عدد الجدران يجب أن يكون بين 1 و 4")
            
            if not 0 <= position <= 10:
                raise ValueError(f"الموضع يجب أن يكون بين 0 و 10")
            
            if not 0 <= angle <= 360:
                raise ValueError(f"الزاوية يجب أن تكون بين 0 و 360")
            
            if rails not in self.custom_positions:
                self.custom_positions[rails] = {}
            
            self.custom_positions[rails][position] = (angle, description)
            
            # مسح ذاكرة التخزين المؤقت للدالة
            self.get_angle_for_rails.cache_clear()
            
            logger.info(f"✅ تم إضافة موضع مخصص: جدران={rails}, موضع={position}, زاوية={angle}°")
        
        except ValueError as e:
            logger.error(f"❌ خطأ في إضافة موضع مخصص: {e}")
            raise
    
    def get_distance_between_positions(self, rails: int, pos1: float, pos2: float) -> float:
        """
        حساب المسافة بين موضعين (مفيد للحسابات الهندسية)
        """
        try:
            angle1 = self.get_angle_for_rails(rails, pos1)
            angle2 = self.get_angle_for_rails(rails, pos2)
            
            # حساب الفرق في الزوايا
            angle_diff = abs(angle2 - angle1)
            
            # منع الالتفاف
            if angle_diff > 180:
                angle_diff = 360 - angle_diff
            
            return angle_diff
        
        except Exception as e:
            logger.error(f"❌ خطأ في حساب المسافة: {e}")
            raise
    
    def clear_interpolation_cache(self):
        """
        مسح ذاكرة الاستيفاء المؤقتة
        """
        try:
            self._interpolation_cache.clear()
            logger.info("✅ تم مسح ذاكرة الاستيفاء المؤقتة")
        except Exception as e:
            logger.error(f"❌ خطأ في مسح الذاكرة: {e}")
    
    def get_cache_stats(self) -> dict:
        """
        الحصول على إحصائيات الذاكرة المؤقتة
        """
        try:
            return {
                "interpolation_cache_size": len(self._interpolation_cache),
                "custom_positions_count": sum(len(v) for v in self.custom_positions.values()),
                "total_rail_positions": sum(len(v) for v in self.RAIL_POSITIONS.values())
            }
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على إحصائيات الذاكرة: {e}")
            return {}
