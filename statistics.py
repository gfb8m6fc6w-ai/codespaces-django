"""
نموذج الإحصائيات
"""

from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime


@dataclass
class Statistics:
    """
    إحصائيات شاملة للمشروع
    
    Attributes:
        total_measurements: إجمالي القياسات
        total_calculations: إجمالي الحسابات
        session_start: وقت بدء الجلسة
        last_update: آخر تحديث
    """
    
    total_measurements: int = 0
    total_calculations: int = 0
    total_shots_attempted: int = 0
    total_shots_successful: int = 0
    average_difficulty: float = 0.0
    session_start: datetime = field(default_factory=datetime.now)
    last_update: datetime = field(default_factory=datetime.now)
    
    # إحصائيات حسب الجدران
    stats_by_rails: Dict[int, dict] = field(default_factory=dict)
    
    # إحصائيات حسب مستوى الصعوبة
    stats_by_difficulty: Dict[str, int] = field(default_factory=dict)
    
    @property
    def session_duration(self) -> float:
        """مدة الجلسة بالثواني"""
        return (datetime.now() - self.session_start).total_seconds()
    
    @property
    def success_rate(self) -> float:
        """معدل النجاح الكلي"""
        if self.total_shots_attempted == 0:
            return 0.0
        return (self.total_shots_successful / self.total_shots_attempted) * 100
    
    def to_dict(self) -> dict:
        """تحويل الإحصائيات إلى قاموس"""
        return {
            'total_measurements': self.total_measurements,
            'total_calculations': self.total_calculations,
            'total_shots_attempted': self.total_shots_attempted,
            'total_shots_successful': self.total_shots_successful,
            'average_difficulty': self.average_difficulty,
            'success_rate': self.success_rate,
            'session_duration': self.session_duration,
            'session_start': self.session_start.isoformat(),
            'last_update': self.last_update.isoformat(),
            'stats_by_rails': self.stats_by_rails,
            'stats_by_difficulty': self.stats_by_difficulty,
        }
