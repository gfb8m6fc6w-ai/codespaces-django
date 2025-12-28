"""
نظام مواضع الجدران المحسّن

يدير جميع الحسابات المتعلقة بمواضع الجدران والزوايا
في لعبة البلياردو بنظام الدايمند العشري
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import logging

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
    نظام مواضع الجدران في البلياردو
    يدير جميع الحسابات المتعلقة بالجدران والزوايا
    """
    
    RAIL_POSITIONS: Dict[int, Dict[float, Tuple[float, str]]] = {
        1: {
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
        2: {
            0.0: (0, "الجدار الأول والثاني - الزاوية"),
            2.5: (45, "موضع 2.5"),
            5.0: (90, "الوسط"),
            7.5: (135, "موضع 7.5"),
            10.0: (180, "الجدار الأول والثاني - الزاوية"),
        },
        3: {
            0.0: (0, "الزاوية الأولى"),
            3.33: (60, "موضع متوسط"),
            6.67: (120, "موضع متوسط"),
            10.0: (180, "الزاوية الثانية"),
        },
        4: {
            0.0: (0, "الزاوية الأولى"),
            2.5: (45, "موضع"),
            5.0: (90, "الوسط"),
            7.5: (135, "موضع"),
            10.0: (180, "الزاوية الثانية"),
        },
    }
    
    def __init__(self):
        """تهيئة نظام الجدران"""
        self.custom_positions: Dict[int, Dict[float, RailPosition]] = {}
        logger.info("✅ نظام الجدران تم تهيئته")
    
    def get_position(self, rails: int, position: float) -> Optional[RailPosition]:
        """
        الحصول على معلومات موضع معين
        
        Args:
            rails: عدد الجدران (1-4)
            position: الموضع على الدايمند (0-10)
        
        Returns:
            كائن RailPosition يحتوي على معلومات الموضع
        
        Raises:
            ValueError: إذا كانت المدخلات غير صحيحة
        """
        if not (1 <= rails <= 4):
            raise ValueError("عدد الجدران يجب أن يكون بين 1 و 4")
        
        if not (0 <= position <= 10):
            raise ValueError("الموضع يجب أن يكون بين 0 و 10")
        
        # البحث في المواضع المخصصة أولاً
        if rails in self.custom_positions and position in self.custom_positions[rails]:
            return self.custom_positions[rails][position]
        
        # البحث في المواضع الافتراضية
        if rails in self.RAIL_POSITIONS and position in self.RAIL_POSITIONS[rails]:
            angle, desc = self.RAIL_POSITIONS[rails][position]
            return RailPosition(rail=rails, position=position, angle=angle, description=desc)
        
        # حساب الموضع بالاستيفاء
        return self._interpolate_position(rails, position)
    
    def _interpolate_position(self, rails: int, position: float) -> RailPosition:
        """
        حساب موضع بالاستيفاء الخطي بين المواضع المعروفة
        
        Args:
            rails: عدد الجدران
            position: الموضع
        
        Returns:
            RailPosition محسوب
        """
        positions = sorted(self.RAIL_POSITIONS[rails].keys())
        
        for i in range(len(positions) - 1):
            if positions[i] <= position <= positions[i + 1]:
                p1, p2 = positions[i], positions[i + 1]
                angle1, _ = self.RAIL_POSITIONS[rails][p1]
                angle2, _ = self.RAIL_POSITIONS[rails][p2]
                
                # الاستيفاء الخطي
                t = (position - p1) / (p2 - p1) if p2 != p1 else 0
                angle = angle1 + (angle2 - angle1) * t
                
                return RailPosition(
                    rail=rails,
                    position=position,
                    angle=angle,
                    description=f"موضع محسوب: {position} على {rails} جدران"
                )
        
        # في الحالات الحدية
        return RailPosition(rail=rails, position=position, angle=0, description="موضع حدي")
    
    def get_all_positions(self, rails: int) -> List[RailPosition]:
        """
        الحصول على جميع المواضع المعروفة لعدد جدران معين
        
        Args:
            rails: عدد الجدران (1-4)
        
        Returns:
            قائمة RailPosition مرتبة حسب الموضع
        """
        if rails not in self.RAIL_POSITIONS:
            raise ValueError(f"لا توجد مواضع لـ {rails} جدران")
        
        positions = []
        for pos in self.RAIL_POSITIONS[rails].keys():
            positions.append(self.get_position(rails, pos))
        return sorted(positions, key=lambda p: p.position)
    
    def calculate_angle_difference(self, rails: int, pos1: float, pos2: float) -> float:
        """
        حساب الفرق في الزاوية بين موضعين
        
        Args:
            rails: عدد الجدران
            pos1: الموضع الأول
            pos2: الموضع الثاني
        
        Returns:
            فرق الزاوية بالدرجات
        """
        p1 = self.get_position(rails, pos1)
        p2 = self.get_position(rails, pos2)
        return abs(p2.angle - p1.angle)
    
    def add_custom_position(self, rails: int, position: RailPosition) -> None:
        """
        إضافة موضع مخصص
        
        Args:
            rails: عدد الجدران
            position: كائن RailPosition
        """
        if rails not in self.custom_positions:
            self.custom_positions[rails] = {}
        self.custom_positions[rails][position.position] = position
        logger.info(f"✅ موضع مخصص أضيف: {position.description}")
