"""
نموذج القياس (Measurement)
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Measurement:
    """
    تمثيل قياس من قاعدة البيانات
    
    Attributes:
        id (str): معرف فريد للقياس
        rail (int): عدد الجدران
        cue_value (float): قيمة العصا
        white_ball_value (float): قيمة الكرة البيضاء
        pocket (int): رقم الجيب
        difficulty_level (int): مستوى الصعوبة (1-5)
        success_rate (float): معدل النجاح المتوقع
        description (str): وصف للقياس
    """
    
    id: str
    rail: int
    cue_value: float
    white_ball_value: float
    pocket: int
    difficulty_level: int = field(default=3)
    success_rate: float = field(default=50.0)
    description: str = field(default="")
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """تحويل القياس إلى قاموس"""
        return {
            'id': self.id,
            'rail': self.rail,
            'cue_value': self.cue_value,
            'white_ball_value': self.white_ball_value,
            'pocket': self.pocket,
            'difficulty_level': self.difficulty_level,
            'success_rate': self.success_rate,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Measurement':
        """إنشاء قياس من قاموس"""
        return cls(**data)
