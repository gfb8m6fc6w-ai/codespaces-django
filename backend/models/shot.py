"""
نموذج التسديقة (Shot) المحسّن

يمثل تسديقة البلياردو مع جميع معاملات الحساب
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


class Difficulty(Enum):
    """مستويات صعوبة التسديقة"""
    EASY = "سهلة"
    MEDIUM = "متوسطة"
    HARD = "صعبة"
    VERY_HARD = "جداً صعبة"
    EXTREME = "قصوى"


class ShotResult(Enum):
    """نتائج التسديقة"""
    SUCCESSFUL = "نجاح"
    FAILED = "فشل"
    PARTIAL = "جزئي"
    PENDING = "معلق"


@dataclass
class Shot:
    """
    تمثيل التسديقة الكاملة مع جميع المعاملات
    """
    
    rails: int
    cue_position: float
    white_ball: float
    target: float
    pocket: int
    difficulty: Difficulty = field(default=Difficulty.MEDIUM)
    success_rate: float = field(default=50.0)
    executed: bool = field(default=False)
    result: Optional[ShotResult] = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)
    notes: str = field(default="")
    
    def __post_init__(self):
        """التحقق من صحة البيانات عند الإنشاء"""
        self.validate()
    
    def validate(self) -> bool:
        """
        التحقق من صحة معاملات التسديقة
        
        Returns:
            True إذا كانت جميع المعاملات صحيحة
        
        Raises:
            ValueError: إذا كانت أي معاملة غير صحيحة
        """
        if not (1 <= self.rails <= 4):
            raise ValueError("عدد الجدران يجب أن يكون بين 1 و 4")
        
        if not (0 <= self.cue_position <= 10):
            raise ValueError("موضع العصا يجب أن يكون بين 0 و 10")
        
        if not (0 <= self.white_ball <= 10):
            raise ValueError("موضع الكرة البيضاء يجب أن يكون بين 0 و 10")
        
        if not (0 <= self.target <= 10):
            raise ValueError("موضع الهدف يجب أن يكون بين 0 و 10")
        
        if not (0 <= self.pocket <= 5):
            raise ValueError("موضع الجيب يجب أن يكون بين 0 و 5")
        
        if not (0 <= self.success_rate <= 100):
            raise ValueError("معدل النجاح يجب أن يكون بين 0 و 100")
        
        return True
    
    def to_dict(self) -> dict:
        """تحويل التسديقة إلى قاموس للحفظ"""
        return {
            'rails': self.rails,
            'cue_position': self.cue_position,
            'white_ball': self.white_ball,
            'target': self.target,
            'pocket': self.pocket,
            'difficulty': self.difficulty.value,
            'success_rate': self.success_rate,
            'executed': self.executed,
            'result': self.result.value if self.result else None,
            'timestamp': self.timestamp.isoformat(),
            'notes': self.notes,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Shot':
        """
        إنشاء تسديقة من قاموس
        
        Args:
            data: قاموس يحتوي على بيانات التسديقة
        
        Returns:
            كائن Shot
        """
        try:
            data_copy = data.copy()
            
            # تحويل الصعوبة
            if isinstance(data_copy.get('difficulty'), str):
                for d in Difficulty:
                    if d.value == data_copy['difficulty']:
                        data_copy['difficulty'] = d
                        break
            
            # تحويل النتيجة
            if isinstance(data_copy.get('result'), str):
                for r in ShotResult:
                    if r.value == data_copy['result']:
                        data_copy['result'] = r
                        break
            
            # تحويل التوقيت
            if isinstance(data_copy.get('timestamp'), str):
                data_copy['timestamp'] = datetime.fromisoformat(data_copy['timestamp'])
            
            return cls(**data_copy)
        except Exception as e:
            logger.error(f"❌ خطأ في إنشاء تسديقة من قاموس: {e}")
            raise


@dataclass
class ShotStatistics:
    """إحصائيات التسديقات"""
    total_shots: int = 0
    successful_shots: int = 0
    failed_shots: int = 0
    partial_shots: int = 0
    average_success_rate: float = 0.0
    
    @property
    def success_percentage(self) -> float:
        """حساب نسبة النجاح"""
        if self.total_shots == 0:
            return 0.0
        return (self.successful_shots / self.total_shots) * 100
    
    def to_dict(self) -> dict:
        """تحويل الإحصائيات إلى قاموس"""
        return {
            'total_shots': self.total_shots,
            'successful_shots': self.successful_shots,
            'failed_shots': self.failed_shots,
            'partial_shots': self.partial_shots,
            'average_success_rate': self.average_success_rate,
            'success_percentage': self.success_percentage,
        }
