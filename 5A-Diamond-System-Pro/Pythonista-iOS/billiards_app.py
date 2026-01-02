#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق البلياردو المتكامل لـ Pythonista 3
Complete Billiards Calculator App for Pythonista

مميزات التطبيق:
- حساب التسديدات المتقدمة
- إدارة الإحصائيات
- واجهة رسومية سهلة الاستخدام
- التخزين المحلي للبيانات
- دعم اللغة العربية الكامل
"""

import ui
import json
import os
from datetime import datetime
from pathlib import Path
import math

# ==================== نموذج البيانات ====================

class Shot:
    """نموذج التسديدة"""
    
    def __init__(self, angle: float = 0, power: float = 0, 
                 distance: float = 0, difficulty: int = 1):
        self.angle = angle
        self.power = power
        self.distance = distance
        self.difficulty = difficulty
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'angle': self.angle,
            'power': self.power,
            'distance': self.distance,
            'difficulty': self.difficulty,
            'timestamp': self.timestamp
        }

class ShotCalculator:
    """حاسبة التسديدات"""
    
    def __init__(self):
        self.min_angle = -90
        self.max_angle = 90
        self.min_power = 0
        self.max_power = 100
        self.min_distance = 0
        self.max_distance = 300
        self.difficulty_levels = [
            'سهل جداً',
            'سهل',
            'متوسط',
            'صعب',
            'صعب جداً',
            'احترافي'
        ]
    
    def calculate_success_rate(self, angle: float, power: float, 
                              distance: float, difficulty: int) -> float:
        """
        حساب نسبة نجاح التسديدة
        
        Args:
            angle: زاوية التسديدة (-90 إلى 90)
            power: قوة التسديدة (0 إلى 100)
            distance: المسافة إلى الهدف (0 إلى 300)
            difficulty: مستوى الصعوبة (0 إلى 5)
        
        Returns:
            نسبة النجاح من 0 إلى 100
        """
        # تعديل الزاوية (أقرب إلى 0 أفضل)
        angle_factor = 100 - (abs(angle) * 0.5)
        angle_factor = max(0, min(100, angle_factor))
        
        # تعديل القوة (50-70 هي الأمثل)
        if 40 <= power <= 80:
            power_factor = 100
        elif 20 <= power < 40:
            power_factor = 80 + (power - 20) * 1
        elif 80 < power <= 100:
            power_factor = 100 - (power - 80) * 1
        else:
            power_factor = max(0, 40 + power * 0.5)
        
        # تعديل المسافة
        if distance <= 50:
            distance_factor = 100
        elif 50 < distance <= 150:
            distance_factor = 100 - (distance - 50) * 0.3
        else:
            distance_factor = 100 - (distance - 150) * 0.2
        
        distance_factor = max(0, distance_factor)
        
        # تأثير الصعوبة
        difficulty_factor = 100 - (difficulty * 15)
        difficulty_factor = max(10, difficulty_factor)
        
        # الحساب النهائي
        success_rate = (
            (angle_factor * 0.2) +
            (power_factor * 0.3) +
            (distance_factor * 0.3) +
            (difficulty_factor * 0.2)
        )
        
        return min(100, max(0, success_rate))
    
    def calculate_optimal_power(self, distance: float) -> float:
        """حساب القوة المثالية بناءً على المسافة"""
        # الصيغة: Power = 30 + (distance * 0.2)
        power = 30 + (distance * 0.2)
        return min(100, max(0, power))
    
    def get_difficulty_name(self, level: int) -> str:
        """الحصول على اسم مستوى الصعوبة"""
        if 0 <= level < len(self.difficulty_levels):
            return self.difficulty_levels[level]
        return 'غير محدد'

# ==================== مدير البيانات ====================

class DataManager:
    """مدير تخزين واسترجاع البيانات"""
    
    def __init__(self):
        # استخدام مجلد Documents في Pythonista
        self.data_dir = Path(os.path.expanduser('~/Documents/5A-Diamond-System'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.shots_file = self.data_dir / 'shots.json'
        self.stats_file = self.data_dir / 'statistics.json'
    
    def save_shot(self, shot: Shot) -> bool:
        """حفظ التسديدة"""
        try:
            shots = self.load_shots()
            shots.append(shot.to_dict())
            with open(self.shots_file, 'w', encoding='utf-8') as f:
                json.dump(shots, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'خطأ في حفظ التسديدة: {e}')
            return False
    
    def load_shots(self) -> list:
        """تحميل جميع التسديدات"""
        try:
            if self.shots_file.exists():
                with open(self.shots_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f'خطأ في تحميل التسديدات: {e}')
        return []
    
    def clear_all_shots(self) -> bool:
        """حذف جميع التسديدات"""
        try:
            if self.shots_file.exists():
                self.shots_file.unlink()
            return True
        except Exception as e:
            print(f'خطأ في حذف البيانات: {e}')
            return False
    
    def get_statistics(self) -> dict:
        """الحصول على الإحصائيات"""
        shots = self.load_shots()
        if not shots:
            return {
                'total_shots': 0,
                'average_success_rate': 0,
                'best_shot': None,
                'most_used_difficulty': 'لا توجد بيانات'
            }
        
        success_rates = [s.get('success_rate', 0) for s in shots]
        avg_rate = sum(success_rates) / len(success_rates) if success_rates else 0
        
        return {
            'total_shots': len(shots),
            'average_success_rate': round(avg_rate, 2),
            'best_shot': max(shots, key=lambda x: x.get('success_rate', 0)),
            'last_shot': shots[-1] if shots else None
        }

# ==================== الواجهة الرسومية ====================

class BilliardsView(ui.View):
    """الواجهة الرسومية الرئيسية"""
    
    def __init__(self):
        self.calculator = ShotCalculator()
        self.data_manager = DataManager()
        self.current_angle = 0
        self.current_power = 50
        self.current_distance = 100
        self.current_difficulty = 2
        
    def will_close(self):
        """عند إغلاق التطبيق"""
        pass

class MainController(ui.ViewController):
    """المتحكم الرئيسي للتطبيق"""
    
    def __init__(self):
        super().__init__()
        self.calculator = ShotCalculator()
        self.data_manager = DataManager()
        self.view_controller = None
        
    def load_view(self):
        """تحميل الواجهة"""
        self.view = ui.View()
        self.view.background_color = '#1a1a2e'
        
        # العنوان
        title = ui.Label()
        title.text = 'حاسبة البلياردو المتقدمة'
        title.font = ('<system>', 22)
        title.alignment = ui.ALIGN_CENTER
        title.text_color = '#eee'
        title.frame = (20, 30, 280, 40)
        self.view.add_subview(title)
        
        # الزاوية
        angle_label = ui.Label()
        angle_label.text = 'الزاوية (°)'
        angle_label.font = ('<system>', 14)
        angle_label.text_color = '#0f3460'
        angle_label.frame = (20, 80, 280, 25)
        self.view.add_subview(angle_label)
        
        self.angle_field = ui.TextField()
        self.angle_field.placeholder = 'أدخل الزاوية (-90 إلى 90)'
        self.angle_field.keyboard_type = ui.KEYBOARD_DECIMAL_PAD
        self.angle_field.text = '0'
        self.angle_field.frame = (20, 110, 280, 32)
        self.view.add_subview(self.angle_field)
        
        # القوة
        power_label = ui.Label()
        power_label.text = 'القوة (0-100)'
        power_label.font = ('<system>', 14)
        power_label.text_color = '#0f3460'
        power_label.frame = (20, 150, 280, 25)
        self.view.add_subview(power_label)
        
        self.power_field = ui.TextField()
        self.power_field.placeholder = 'أدخل قوة التسديدة'
        self.power_field.keyboard_type = ui.KEYBOARD_DECIMAL_PAD
        self.power_field.text = '50'
        self.power_field.frame = (20, 180, 280, 32)
        self.view.add_subview(self.power_field)
        
        # المسافة
        distance_label = ui.Label()
        distance_label.text = 'المسافة (سم)'
        distance_label.font = ('<system>', 14)
        distance_label.text_color = '#0f3460'
        distance_label.frame = (20, 220, 280, 25)
        self.view.add_subview(distance_label)
        
        self.distance_field = ui.TextField()
        self.distance_field.placeholder = 'أدخل المسافة'
        self.distance_field.keyboard_type = ui.KEYBOARD_DECIMAL_PAD
        self.distance_field.text = '100'
        self.distance_field.frame = (20, 250, 280, 32)
        self.view.add_subview(self.distance_field)
        
        # الصعوبة
        difficulty_label = ui.Label()
        difficulty_label.text = 'مستوى الصعوبة'
        difficulty_label.font = ('<system>', 14)
        difficulty_label.text_color = '#0f3460'
        difficulty_label.frame = (20, 290, 280, 25)
        self.view.add_subview(difficulty_label)
        
        self.difficulty_segmented = ui.SegmentedControl()
        self.difficulty_segmented.segments = [
            'سهل', 'متوسط', 'صعب', 'احترافي'
        ]
        self.difficulty_segmented.selected_index = 1
        self.difficulty_segmented.frame = (20, 320, 280, 32)
        self.view.add_subview(self.difficulty_segmented)
        
        # زر الحساب
        calculate_btn = ui.Button(title='حساب نسبة النجاح')
        calculate_btn.frame = (20, 360, 280, 44)
        calculate_btn.tint_color = '#16c784'
        calculate_btn.action = self.calculate_success
        self.view.add_subview(calculate_btn)
        
        # النتيجة
        self.result_label = ui.Label()
        self.result_label.text = 'انقر على زر الحساب'
        self.result_label.font = ('<system>', 16)
        self.result_label.text_color = '#16c784'
        self.result_label.alignment = ui.ALIGN_CENTER
        self.result_label.frame = (20, 410, 280, 60)
        self.view.add_subview(self.result_label)
        
        # الأزرار الإضافية
        stats_btn = ui.Button(title='الإحصائيات')
        stats_btn.frame = (20, 480, 135, 44)
        stats_btn.tint_color = '#0f3460'
        stats_btn.action = self.show_statistics
        self.view.add_subview(stats_btn)
        
        reset_btn = ui.Button(title='مسح البيانات')
        reset_btn.frame = (165, 480, 135, 44)
        reset_btn.tint_color = '#e94560'
        reset_btn.action = self.clear_data
        self.view.add_subview(reset_btn)
    
    def calculate_success(self, sender):
        """حساب نسبة النجاح"""
        try:
            angle = float(self.angle_field.text or 0)
            power = float(self.power_field.text or 50)
            distance = float(self.distance_field.text or 100)
            difficulty = self.difficulty_segmented.selected_index + 1
            
            # التحقق من الحدود
            if not (-90 <= angle <= 90):
                self.result_label.text = 'الزاوية يجب أن تكون بين -90 و 90'
                return
            if not (0 <= power <= 100):
                self.result_label.text = 'القوة يجب أن تكون بين 0 و 100'
                return
            if distance < 0:
                self.result_label.text = 'المسافة لا يمكن أن تكون سالبة'
                return
            
            # حساب النجاح
            success_rate = self.calculator.calculate_success_rate(
                angle, power, distance, difficulty
            )
            
            # حفظ التسديدة
            shot = Shot(angle, power, distance, difficulty)
            shot.success_rate = success_rate
            self.data_manager.save_shot(shot)
            
            # عرض النتيجة
            self.result_label.text = f'نسبة النجاح: {success_rate:.1f}%'
            
        except ValueError:
            self.result_label.text = 'تحقق من صحة الأرقام المدخلة'
    
    def show_statistics(self, sender):
        """عرض الإحصائيات"""
        stats = self.data_manager.get_statistics()
        
        message = f"""
الإحصائيات الكاملة
━━━━━━━━━━━━━━━
            إجمالي التسديدات: {stats['total_shots']}
متوسط النجاح: {stats['average_success_rate']}%

آخر تسديقة:
{self._format_shot(stats['last_shot'])}
        """
        
        ui.alert_message('الإحصائيات', message)
    
    def clear_data(self, sender):
        """مسح البيانات"""
        def confirm(action):
            if action == 1:
                self.data_manager.clear_all_shots()
                self.result_label.text = 'تم مسح جميع البيانات'
                ui.alert_message('تم', 'تم حذف جميع التسديدات بنجاح')
        
        ui.alert_action('تأكيد', 'هل تريد حذف جميع البيانات؟', 
                       actions=['إلغاء', 'حذف'], completion=confirm)
    
    def _format_shot(self, shot: dict) -> str:
        """تنسيق بيانات التسديدة للعرض"""
        if not shot:
            return 'لا توجد بيانات'
        return f"""
الزاوية: {shot['angle']}°
القوة: {shot['power']}
المسافة: {shot['distance']} سم
        """

# ==================== نقطة الدخول ====================

def main():
    """تشغيل التطبيق"""
    controller = MainController()
    nav = ui.NavigationController(controller)
    nav.navigation_bar.title_attributes = {
        ui.ATTR_FONT: ('<system>', 18),
        ui.ATTR_TEXT_COLOR: '#eee'
    }
    nav.present('sheet')

if __name__ == '__main__':
    main()
