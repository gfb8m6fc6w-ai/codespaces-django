#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API REST للنظام الخلفي
Billiards REST API Backend
"""

import json
from typing import Dict, List, Optional
from datetime import datetime

class Shot:
    """نموذج التسديقة"""
    def __init__(self, angle, power, distance, difficulty):
        self.angle = angle
        self.power = power
        self.distance = distance
        self.difficulty = difficulty
        self.timestamp = datetime.now().isoformat()
        self.id = int(datetime.now().timestamp() * 1000)
    
    def to_dict(self):
        return {
            'id': self.id,
            'angle': self.angle,
            'power': self.power,
            'distance': self.distance,
            'difficulty': self.difficulty,
            'timestamp': self.timestamp
        }

class BilliardsCalculator:
    """حاسبة البلياردو"""
    
    def calculate_success_rate(self, angle: float, power: float, 
                              distance: float, difficulty: int) -> float:
        """حساب نسبة النجاح"""
        angle_factor = 100 - (abs(angle) / 90 * 50)
        
        if 40 <= power <= 70:
            power_factor = 100
        elif 20 <= power < 40:
            power_factor = 60 + (power - 20) * 2
        elif 70 < power <= 100:
            power_factor = 100 - (power - 70) * 1.5
        else:
            power_factor = max(0, power)
        
        if distance <= 50:
            distance_factor = 100
        elif distance <= 200:
            distance_factor = 100 - (distance - 50) * 0.25
        else:
            distance_factor = 100 - (distance - 200) * 0.1
        
        difficulty_factors = [150, 120, 100, 80, 60, 40]
        difficulty_factor = difficulty_factors[difficulty] if difficulty < len(difficulty_factors) else 100
        
        success_rate = (
            angle_factor * 0.25 +
            power_factor * 0.25 +
            distance_factor * 0.25 +
            difficulty_factor * 0.25
        )
        
        return min(100, max(0, success_rate))

class BilliardsAPI:
    """واجهة API البلياردو"""
    
    def __init__(self):
        self.calculator = BilliardsCalculator()
        self.shots = []
    
    def calculate_shot(self, angle: float, power: float, 
                      distance: float, difficulty: int) -> Dict:
        """حساب تسديقة جديدة"""
        success_rate = self.calculator.calculate_success_rate(
            angle, power, distance, difficulty
        )
        
        shot = Shot(angle, power, distance, difficulty)
        shot.success_rate = success_rate
        self.shots.append(shot)
        
        return {
            'success': True,
            'shot': shot.to_dict(),
            'success_rate': success_rate,
            'recommendation': self._get_recommendation(success_rate)
        }
    
    def get_statistics(self) -> Dict:
        """الحصول على الإحصائيات"""
        if not self.shots:
            return {
                'total_shots': 0,
                'avg_success_rate': 0,
                'best_shot': None,
                'worst_shot': None
            }
        
        success_rates = [s.success_rate for s in self.shots]
        
        return {
            'total_shots': len(self.shots),
            'avg_success_rate': sum(success_rates) / len(success_rates),
            'best_shot': max(self.shots, key=lambda s: s.success_rate).to_dict(),
            'worst_shot': min(self.shots, key=lambda s: s.success_rate).to_dict()
        }
    
    def _get_recommendation(self, success_rate: float) -> str:
        """توصيات بناءً على معدل النجاح"""
        if success_rate >= 80:
            return 'ممتاز! احفظ هذه الطريقة'
        elif success_rate >= 60:
            return 'جيد جداً، يمكن تحسينها أكثر'
        elif success_rate >= 40:
            return 'معقول، جرب تعديل القوة'
        else:
            return 'عليك تحسين الزاوية والقوة'

# تصدير API
api = BilliardsAPI()
