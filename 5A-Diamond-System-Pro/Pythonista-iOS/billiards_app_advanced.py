#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق البلياردو المتقدم - نسخة Pythonista الكاملة المُصلّحة
Advanced Billiards App - Fixed & Enhanced Pythonista Edition

المميزات المتقدمة:
✅ حسابات متقدمة للتسديدات
✅ نظام السجلات التفصيلي
✅ تحليل الأداء والاتجاهات
✅ توقعات ذكية وتوصيات
✅ واجهة رسومية احترافية بتبويبات
✅ دعم اللغة العربية الكامل
✅ حفظ وتحميل البيانات تلقائياً
✅ إحصائيات شاملة ومتقدمة
"""

import ui
import json
import console
import dialogs
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import math

# ==================== ثوابت التطبيق ====================

# الألوان
COLOR_BG = '#1a1a2e'
COLOR_TEXT = '#eee'
COLOR_PRIMARY = '#16c784'
COLOR_SECONDARY = '#0f3460'
COLOR_DANGER = '#e94560'
COLOR_ACCENT = '#f39c12'

# نطاقات القيم
ANGLE_MIN, ANGLE_MAX = -90, 90
POWER_MIN, POWER_MAX = 0, 100
DISTANCE_MIN, DISTANCE_MAX = 0, 500

# مستويات الصعوبة
DIFFICULTY_LEVELS = [
    {'id': 0, 'name': 'سهل جداً', 'factor': 1.5},
    {'id': 1, 'name': 'سهل', 'factor': 1.2},
    {'id': 2, 'name': 'متوسط', 'factor': 1.0},
    {'id': 3, 'name': 'صعب', 'factor': 0.8},
    {'id': 4, 'name': 'صعب جداً', 'factor': 0.6},
    {'id': 5, 'name': 'احترافي', 'factor': 0.4}
]

# ==================== نماذج البيانات ====================

class Shot:
    """نموذج التسديدة المتقدم"""
    
    def __init__(self, angle=0, power=0, distance=0, difficulty=2, 
                 cue_type='عادي', success=None):
        self.angle = float(angle)
        self.power = float(power)
        self.distance = float(distance)
        self.difficulty = int(difficulty)
        self.cue_type = cue_type
        self.success_rate = success  # ✅ اسم الخاصية الصحيح
        self.timestamp = datetime.now().isoformat()
        self.id = int(datetime.now().timestamp() * 1000)
    
    def to_dict(self):
        return {
            'id': self.id,
            'angle': self.angle,
            'power': self.power,
            'distance': self.distance,
            'difficulty': self.difficulty,
            'cue_type': self.cue_type,
            'success_rate': self.success_rate,  # ✅ الحفظ الصحيح
            'timestamp': self.timestamp
        }
    
    @staticmethod
    def from_dict(data):
        shot = Shot(
            angle=data.get('angle', 0),
            power=data.get('power', 0),
            distance=data.get('distance', 0),
            difficulty=data.get('difficulty', 2),
            cue_type=data.get('cue_type', 'عادي'),
            success=data.get('success_rate')  # ✅ المفتاح الصحيح
        )
        shot.timestamp = data.get('timestamp', shot.timestamp)
        shot.id = data.get('id', shot.id)
        return shot

class AdvancedCalculator:
    """حاسبة التسديدات المتقدمة"""
    
    def __init__(self):
        self.cue_types = {
            'عادي': {'spin_factor': 1.0, 'accuracy': 1.0},
            'بدوران إمامي': {'spin_factor': 1.3, 'accuracy': 0.9},
            'بدوران خلفي': {'spin_factor': 1.1, 'accuracy': 0.95},
            'دقيق': {'spin_factor': 0.9, 'accuracy': 1.2}
        }
    
    def calculate_success_rate(self, angle, power, distance, difficulty, 
                              cue_type='عادي'):
        """
        حساب شامل لنسبة نجاح التسديدة
        
        المعادلة:
        Success = (Angle × 0.25) + (Power × 0.25) + (Distance × 0.25) + (Difficulty × 0.25)
        """
        # تأثير الزاوية
        angle_factor = self._calculate_angle_factor(angle)
        
        # تأثير القوة
        power_factor = self._calculate_power_factor(power)
        
        # تأثير المسافة
        distance_factor = self._calculate_distance_factor(distance)
        
        # تأثير الصعوبة
        difficulty_data = DIFFICULTY_LEVELS[difficulty]
        difficulty_factor = 100 * difficulty_data['factor']
        
        # تأثير نوع العصا
        cue_data = self.cue_types.get(cue_type, self.cue_types['عادي'])
        
        # الحساب النهائي
        base_success = (
            angle_factor * 0.25 +
            power_factor * 0.25 +
            distance_factor * 0.25 +
            difficulty_factor * 0.25
        )
        
        # تطبيق معاملات العصا
        final_success = base_success * cue_data['accuracy']
        
        return min(100, max(0, final_success))
    
    def _calculate_angle_factor(self, angle):
        """حساب تأثير الزاوية"""
        angle_penalty = abs(angle) / 90 * 50
        return 100 - angle_penalty
    
    def _calculate_power_factor(self, power):
        """حساب تأثير القوة"""
        if power < 0 or power > 100:
            return 0
        
        if 40 <= power <= 70:
            return 100
        elif 20 <= power < 40:
            return 60 + (power - 20) * 2
        elif 70 < power <= 100:
            return 100 - (power - 70) * 1.5
        else:
            return power
    
    def _calculate_distance_factor(self, distance):
        """حساب تأثير المسافة"""
        if distance <= 50:
            return 100
        elif 50 < distance <= 200:
            return 100 - (distance - 50) * 0.25
        else:
            return 100 - (distance - 200) * 0.1
    
    def recommend_power(self, distance):
        """توصية بالقوة المثالية"""
        return min(100, 40 + (distance * 0.15))
    
    def analyze_trend(self, shots):
        """تحليل الاتجاهات في الأداء"""
        if len(shots) < 3:
            return {'trend': 'محدود', 'improvement': 0}
        
        recent = shots[-10:] if len(shots) > 10 else shots
        success_rates = [s.success for s in recent if s.success is not None]
        
        if not success_rates:
            return {'trend': 'محدود', 'improvement': 0}
        
        avg_recent = sum(success_rates) / len(success_rates)
        
        if len(shots) > 10:
            older = shots[-20:-10]
            older_rates = [s.success for s in older if s.success is not None]
            avg_older = sum(older_rates) / len(older_rates) if older_rates else 50
        else:
            avg_older = 50
        
        improvement = avg_recent - avg_older
        
        if improvement > 5:
            trend = 'تحسن ملحوظ ⬆️'
        elif improvement < -5:
            trend = 'تراجع ملحوظ ⬇️'
        else:
            trend = 'مستقر ➡️'
        
        return {'trend': trend, 'improvement': improvement}

class AdvancedDataManager:
    """مدير البيانات المتقدم"""
    
    def __init__(self):
        self.data_dir = Path(os.path.expanduser('~/Documents/5A-Diamond-System'))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.shots_file = self.data_dir / 'shots.json'
        self.sessions_file = self.data_dir / 'sessions.json'
    
    def save_shot(self, shot):
        """حفظ التسديدة مع معالجة الأخطاء"""
        try:
            shots = self.load_shots()
            shots.append(shot.to_dict())
            with open(self.shots_file, 'w', encoding='utf-8') as f:
                json.dump(shots, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            console.print_message(f'خطأ في حفظ التسديدة: {e}', color=(1, 0, 0))
            return False
    
    def load_shots(self):
        """تحميل التسديدات"""
        try:
            if self.shots_file.exists():
                with open(self.shots_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def get_shots_list(self):
        """الحصول على قائمة التسديدات"""
        data = self.load_shots()
        return [Shot.from_dict(d) for d in data]
    
    def get_statistics(self):
        """الحصول على الإحصائيات الشاملة"""
        shots = self.get_shots_list()
        
        if not shots:
            return {
                'total_shots': 0,
                'successful_shots': 0,
                'success_rate': 0,
                'avg_success': 0,
                'best_shot': None,
                'worst_shot': None,
                'favorite_difficulty': 'لا توجد بيانات'
            }
        
        total = len(shots)
        with_success = [s for s in shots if s.success_rate is not None]
        
        if with_success:
            success_rates = [s.success_rate for s in with_success]
            avg_success = sum(success_rates) / len(success_rates)
            best_shot = max(with_success, key=lambda s: s.success_rate or 0)
            worst_shot = min(with_success, key=lambda s: s.success_rate or 0)
        else:
            avg_success = 0
            best_shot = None
            worst_shot = None
        
        # حساب آخر 10
        last_10_rates = [s.success_rate for s in shots[-10:] if s.success_rate]
        last_10_avg = sum(last_10_rates) / len(last_10_rates) if last_10_rates else 0
        
        # تحليل الاتجاه
        trend = self._analyze_trend(shots)
        
        return {
            'total_shots': total,
            'successful_shots': len(with_success),
            'success_rate': (len(with_success) / total * 100) if total > 0 else 0,
            'avg_success': avg_success,
            'best_shot': best_shot,
            'worst_shot': worst_shot,
            'last_10_avg': last_10_avg,
            'trend': trend
        }
    
    def _analyze_trend(self, shots):
        """تحليل الاتجاه في الأداء"""
        if len(shots) < 5:
            return 'محدود'
        
        recent = shots[-10:] if len(shots) > 10 else shots
        recent_rates = [s.success_rate for s in recent if s.success_rate]
        
        if not recent_rates:
            return 'محدود'
        
        avg_recent = sum(recent_rates) / len(recent_rates)
        
        if len(shots) > 10:
            older = shots[-20:-10]
            older_rates = [s.success_rate for s in older if s.success_rate]
            avg_older = sum(older_rates) / len(older_rates) if older_rates else 50
        else:
            avg_older = 50
        
        improvement = avg_recent - avg_older
        
        if improvement > 10:
            return 'تحسن كبير ⬆️'
        elif improvement > 0:
            return 'تحسن ملحوظ ⬆️'
        elif improvement < -10:
            return 'تراجع كبير ⬇️'
        elif improvement < 0:
            return 'تراجع ملحوظ ⬇️'
        else:
            return 'مستقر ➡️'
    
    def clear_data(self):
        """حذف جميع البيانات"""
        try:
            if self.file_path.exists():
                self.file_path.unlink()
            console.print_message('تم مسح جميع البيانات بنجاح', color=(0, 1, 0))
            return True
        except Exception as e:
            console.print_message(f'خطأ في مسح البيانات: {e}', color=(1, 0, 0))
            return False

class TabViewController(ui.ViewController):
    """عارض التبويبات"""
    
    def __init__(self):
        super().__init__()
        self.calculator = AdvancedCalculator()
        self.data_manager = AdvancedDataManager()
    
    def load_view(self):
        """تحميل الواجهة بالكامل"""
        self.view = ui.View()
        self.view.background_color = COLOR_BG
        
        self.create_header()
        
        self.content_container = ui.View()
        self.content_container.frame = (0, 60, self.view.width, self.view.height - 120)
        self.view.add_subview(self.content_container)
        
        self.create_tab_bar()
        
        self.show_calculator_tab()
    
    def create_header(self):
        """إنشء رأس الصفحة"""
        header = ui.View()
        header.background_color = COLOR_SECONDARY
        header.frame = (0, 0, self.view.width, 60)
        self.view.add_subview(header)
        
        title = ui.Label()
        title.text = 'حاسبة البلياردو المتقدمة'
        title.font = ('<system>', 18)
        title.text_color = COLOR_TEXT
        title.alignment = ui.ALIGN_CENTER
        title.frame = (0, 10, self.view.width, 40)
        header.add_subview(title)
    
    def create_tab_bar(self):
        """إنشء شريط التبويبات"""
        tabbar = ui.View()
        tabbar.background_color = COLOR_SECONDARY
        tabbar.frame = (0, self.view.height - 60, self.view.width, 60)
        self.view.add_subview(tabbar)
        
        tab_width = self.view.width / 3
        
        btn1 = ui.Button(title='📊 حساب')
        btn1.frame = (0, 0, tab_width, 60)
        btn1.tint_color = COLOR_PRIMARY
        btn1.action = lambda: self.switch_tab(0)
        tabbar.add_subview(btn1)
        
        btn2 = ui.Button(title='📈 إحصائيات')
        btn2.frame = (tab_width, 0, tab_width, 60)
        btn2.tint_color = COLOR_ACCENT
        btn2.action = lambda: self.switch_tab(1)
        tabbar.add_subview(btn2)
        
        btn3 = ui.Button(title='⚙️ إعدادات')
        btn3.frame = (tab_width * 2, 0, tab_width, 60)
        btn3.tint_color = COLOR_DANGER
        btn3.action = lambda: self.switch_tab(2)
        tabbar.add_subview(btn3)
    
    def switch_tab(self, tab_id):
        """التبديل بين التبويبات"""
        for subview in list(self.content_container.subviews):
            subview.remove_from_superview()
        
        if tab_id == 0:
            self.show_calculator_tab()
        elif tab_id == 1:
            self.show_statistics_tab()
        elif tab_id == 2:
            self.show_settings_tab()
    
    def show_calculator_tab(self):
        """عرض علامة تبويب الحساب"""
        y = 10
        
        angle_label = ui.Label()
        angle_label.text = 'الزاوية (°)'
        angle_label.font = ('<system>', 12)
        angle_label.text_color = COLOR_SECONDARY
        angle_label.frame = (10, y, 280, 20)
        self.content_container.add_subview(angle_label)
        y += 25
        
        self.angle_slider = ui.Slider()
        self.angle_slider.min_value = ANGLE_MIN
        self.angle_slider.max_value = ANGLE_MAX
        self.angle_slider.value = 0
        self.angle_slider.frame = (10, y, 280, 32)
        self.content_container.add_subview(self.angle_slider)
        y += 40
        
        power_label = ui.Label()
        power_label.text = 'القوة (0-100)'
        power_label.font = ('<system>', 12)
        power_label.text_color = COLOR_SECONDARY
        power_label.frame = (10, y, 280, 20)
        self.content_container.add_subview(power_label)
        y += 25
        
        self.power_slider = ui.Slider()
        self.power_slider.min_value = POWER_MIN
        self.power_slider.max_value = POWER_MAX
        self.power_slider.value = 50
        self.power_slider.frame = (10, y, 280, 32)
        self.content_container.add_subview(self.power_slider)
        y += 40
        
        distance_label = ui.Label()
        distance_label.text = 'المسافة (سم)'
        distance_label.font = ('<system>', 12)
        distance_label.text_color = COLOR_SECONDARY
        distance_label.frame = (10, y, 280, 20)
        self.content_container.add_subview(distance_label)
        y += 25
        
        self.distance_slider = ui.Slider()
        self.distance_slider.min_value = DISTANCE_MIN
        self.distance_slider.max_value = DISTANCE_MAX
        self.distance_slider.value = 100
        self.distance_slider.frame = (10, y, 280, 32)
        self.content_container.add_subview(self.distance_slider)
        y += 40
        
        difficulty_label = ui.Label()
        difficulty_label.text = 'مستوى الصعوبة'
        difficulty_label.font = ('<system>', 12)
        difficulty_label.text_color = COLOR_SECONDARY
        difficulty_label.frame = (10, y, 280, 20)
        self.content_container.add_subview(difficulty_label)
        y += 25
        
        self.difficulty_seg = ui.SegmentedControl()
        self.difficulty_seg.segments = [
            'سهل جداً', 'سهل', 'متوسط', 'صعب', 'صعب جداً', 'احترافي'
        ]
        self.difficulty_seg.selected_index = 2
        self.difficulty_seg.frame = (10, y, 280, 32)
        self.content_container.add_subview(self.difficulty_seg)
        y += 40
        
        calc_btn = ui.Button(title='حساب النجاح')
        calc_btn.frame = (10, y, 280, 44)
        calc_btn.tint_color = COLOR_PRIMARY
        calc_btn.action = self.calculate
        self.content_container.add_subview(calc_btn)
        y += 50
        
        self.result_label = ui.Label()
        self.result_label.text = 'انقر على الحساب'
        self.result_label.font = ('<system>', 16)
        self.result_label.text_color = COLOR_PRIMARY
        self.result_label.alignment = ui.ALIGN_CENTER
        self.result_label.frame = (10, y, 280, 80)
        self.content_container.add_subview(self.result_label)
    
    def show_statistics_tab(self):
        """عرض علامة تبويب الإحصائيات"""
        stats = self.data_manager.get_statistics()
        
        y = 10
        
        stat_texts = [
            f'إجمالي التسديدات: {stats["total_shots"]}',
            f'متوسط النجاح: {stats["avg_success"]:.1f}%',
            f'آخر 10: {stats["last_10_avg"]:.1f}%',
            f'نسبة النجاح الكلية: {stats["success_rate"]:.1f}%'
        ]
        
        for text in stat_texts:
            label = ui.Label()
            label.text = text
            label.font = ('<system>', 14)
            label.text_color = COLOR_TEXT
            label.frame = (10, y, 280, 30)
            self.content_container.add_subview(label)
            y += 35
    
    def show_settings_tab(self):
        """عرض علامة تبويب الإعدادات"""
        y = 10
        
        clear_btn = ui.Button(title='مسح جميع البيانات')
        clear_btn.frame = (10, y, 280, 44)
        clear_btn.tint_color = COLOR_DANGER
        clear_btn.action = self.clear_data
        self.content_container.add_subview(clear_btn)
        
        y += 50
        
        info_label = ui.Label()
        info_label.text = 'ملتزمة بحفظ البيانات:\n~/Documents/BilliardsAdvanced/'
        info_label.font = ('<system>', 12)
        info_label.text_color = COLOR_TEXT
        info_label.number_of_lines = 0
        info_label.frame = (10, y, 280, 60)
        self.content_container.add_subview(info_label)
    
    def calculate(self, sender):
        """حساب نسبة النجاح"""
        try:
            angle = self.angle_slider.value
            power = self.power_slider.value
            distance = self.distance_slider.value
            difficulty = self.difficulty_seg.selected_index
            
            success_rate = self.calculator.calculate_success_rate(
                angle, power, distance, difficulty
            )
            
            shot = Shot(angle, power, distance, difficulty, success=success_rate)
            self.data_manager.save_shot(shot)
            
            self.result_label.text = f'✓ نسبة النجاح\n{success_rate:.1f}%'
            
        except Exception as e:
            self.result_label.text = f'خطأ: {str(e)}'
    
    def clear_data(self, sender):
        """مسح البيانات"""
        if self.data_manager.clear_data():
            ui.alert_message('تم', 'تم حذف جميع البيانات')
        else:
            ui.alert_message('خطأ', 'فشل حذف البيانات')

def main():
    """تشغيل البرنامج الرئيسي"""
    controller = TabViewController()
    nav = ui.NavigationController(controller)
    nav.present('sheet')

if __name__ == '__main__':
    main()
