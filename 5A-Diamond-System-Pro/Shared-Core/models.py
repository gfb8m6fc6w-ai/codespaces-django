#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نماذج البيانات المشتركة
Shared Data Models
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class ShotModel:
    """نموذج التسديقة الموحد"""
    angle: float
    power: float
    distance: float
    difficulty: int
    success_rate: Optional[float] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'angle': self.angle,
            'power': self.power,
            'distance': self.distance,
            'difficulty': self.difficulty,
            'success_rate': self.success_rate,
            'timestamp': self.timestamp
        }

@dataclass
class StatisticsModel:
    """نموذج الإحصائيات"""
    total_shots: int
    avg_success_rate: float
    best_shot: Optional[ShotModel] = None
    worst_shot: Optional[ShotModel] = None
    last_shot: Optional[ShotModel] = None
    
    def to_dict(self):
        return {
            'total_shots': self.total_shots,
            'avg_success_rate': self.avg_success_rate,
            'best_shot': self.best_shot.to_dict() if self.best_shot else None,
            'worst_shot': self.worst_shot.to_dict() if self.worst_shot else None,
            'last_shot': self.last_shot.to_dict() if self.last_shot else None
        }

@dataclass
class PlayerModel:
    """نموذج اللاعب"""
    name: str
    level: int
    total_games: int
    win_rate: float
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

class DifficultyLevel:
    """مستويات الصعوبة"""
    VERY_EASY = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    VERY_HARD = 4
    PROFESSIONAL = 5
    
    LABELS = {
        0: 'سهل جداً',
        1: 'سهل',
        2: 'متوسط',
        3: 'صعب',
        4: 'صعب جداً',
        5: 'احترافي'
    }
    
    FACTORS = {
        0: 1.5,
        1: 1.2,
        2: 1.0,
        3: 0.8,
        4: 0.6,
        5: 0.4
    }
    
    @staticmethod
    def get_label(level: int) -> str:
        return DifficultyLevel.LABELS.get(level, 'غير محدد')
    
    @staticmethod
    def get_factor(level: int) -> float:
        return DifficultyLevel.FACTORS.get(level, 1.0)
