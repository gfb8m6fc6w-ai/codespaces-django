"""
نظام مواضع الجدران
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import math


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
            2.5: (45, "موضع"),
            5.0: (90, "الوسط"),
            7.5: (135, "موضع"),
            10.0: (180, "الزاوية الثانية"),
        },
    }
    
    def __init__(self):
        """تهيئة نظام الجدران"""
        self.custom_positions: Dict[int, Dict[float, RailPosition]] = {}
    
    def get_position(self, rails: int, position: float) -> Optional[RailPosition]:
        """
        الحصول على معلومات موضع معين
        
        Args:
            rails: عدد الجدران (1-4)
            position: الموضع على الدايمند (0-10)
        
        Returns:
            معلومات الموضع
        """
        if not (1 <= rails <= 4):
            raise ValueError(f"عدد الجدران يجب أن يكون بين 1 و 4")
        
        if not (0 <= position <= 10):
            raise ValueError(f"الموضع يجب أن يكون بين 0 و 10")
        
        # البحث في المواضع المخصصة أولاً
        if rails in self.custom_positions and position in self.custom_positions[rails]:
            return self.custom_positions[rails][position]
        
        # البحث في المواضع الافتراضية
        if rails in self.RAIL_POSITIONS and position in self.RAIL_POSITIONS[rails]:
            angle, desc = self.RAIL_POSITIONS[rails][position]
            return RailPosition(rail=rails, position=position, angle=angle, description=desc)
        
        # إذا لم يتم العثور على موضع دقيق، حساب الزاوية
        return self._interpolate_position(rails, position)
    
    def _interpolate_position(self, rails: int, position: float) -> RailPosition:
        """
        حساب موضع بالاستيفاء بين المواضع المعروفة
        """
        positions = sorted(self.RAIL_POSITIONS[rails].keys())
        
        for i in range(len(positions) - 1):
            if positions[i] <= position <= positions[i + 1]:
                p1, p2 = positions[i], positions[i + 1]
                angle1, _ = self.RAIL_POSITIONS[rails][p1]
                angle2, _ = self.RAIL_POSITIONS[rails][p2]
                
                # الاستيفاء الخطي
                t = (position - p1) / (p2 - p1)
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
        """الحصول على جميع المواضع لعدد جدران معين"""
        positions = []
        for pos in self.RAIL_POSITIONS.get(rails, {}).keys():
            positions.append(self.get_position(rails, pos))
        return sorted(positions, key=lambda p: p.position)
    
    def calculate_angle_difference(self, rails: int, pos1: float, pos2: float) -> float:
        """
        حساب الفرق في الزاوية بين موضعين
        """
        p1 = self.get_position(rails, pos1)
        p2 = self.get_position(rails, pos2)
        return abs(p2.angle - p1.angle)
    
    def add_custom_position(self, rails: int, position: RailPosition) -> None:
        """إضافة موضع مخصص"""
        if rails not in self.custom_positions:
            self.custom_positions[rails] = {}
        self.custom_positions[rails][position.position] = position
