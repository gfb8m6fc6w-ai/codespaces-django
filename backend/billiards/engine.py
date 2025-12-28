"""
محرك البلياردو الرئيسي المحسّن

يجمع جميع أنظمة البلياردو الفرعية ويوفر واجهة موحدة
"""

from typing import List, Optional, Dict
import json
from pathlib import Path
import logging
import sys

# إضافة مسار المشروع
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from backend.billiards.calculator import ShotCalculator
    from backend.billiards.rail_system import RailPositionsSystem
    from backend.models.shot import Shot
    from backend.models.statistics import Statistics
except ImportError:
    from .calculator import ShotCalculator
    from .rail_system import RailPositionsSystem
    from ..models.shot import Shot
    from ..models.statistics import Statistics

logger = logging.getLogger(__name__)


class BilliardsEngine:
    """
    محرك البلياردو الرئيسي - يجمع جميع الأنظمة الفرعية
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        تهيئة محرك البلياردو
        
        Args:
            data_dir: مسار مجلد البيانات (اختياري)
        """
        self.calculator = ShotCalculator()
        self.rail_system = RailPositionsSystem()
        self.shots: List[Shot] = []
        self.statistics = Statistics()
        
        # إعداد مسار البيانات
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path.home() / ".billiards_pro"
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.shots_file = self.data_dir / "shots.json"
        self.stats_file = self.data_dir / "statistics.json"
        
        # تحميل البيانات الموجودة
        self.load_from_storage()
        logger.info("✅ محرك البلياردو تم تهيئته")
    
    def calculate_shot(self, rails: int, cue_position: float, white_ball: float,
                      target: float, pocket: int) -> Shot:
        """
        حساب وإنشاء تسديقة جديدة
        
        Args:
            rails: عدد الجدران (1-4)
            cue_position: موضع العصا (0-10)
            white_ball: موضع الكرة البيضاء (0-10)
            target: موضع الهدف (0-10)
            pocket: موضع الجيب المستهدف (0-5)
        
        Returns:
            كائن Shot محسوب
        
        Raises:
            ValueError: إذا كانت المدخلات غير صحيحة
        """
        try:
            shot = self.calculator.create_shot(
                rails, cue_position, white_ball, target, pocket
            )
            self.shots.append(shot)
            self.statistics.total_calculations += 1
            self.save_to_storage()
            return shot
        except Exception as e:
            logger.error(f"❌ خطأ في حساب التسديقة: {e}")
            raise
    
    def record_execution(self, shot: Shot, successful: bool) -> None:
        """
        تسجيل نتيجة تنفيذ التسديقة
        
        Args:
            shot: التسديقة
            successful: هل كانت ناجحة؟
        """
        try:
            shot.executed = True
            self.statistics.total_shots_attempted += 1
            
            if successful:
                self.statistics.total_shots_successful += 1
            
            self.save_to_storage()
            logger.info(f"✅ تم تسجيل النتيجة: {'نجاح' if successful else 'فشل'}")
        except Exception as e:
            logger.error(f"❌ خطأ في تسجيل النتيجة: {e}")
            raise
    
    def get_shots_by_difficulty(self, difficulty: str) -> List[Shot]:
        """
        الحصول على التسديقات حسب مستوى الصعوبة
        
        Args:
            difficulty: مستوى الصعوبة
        
        Returns:
            قائمة التسديقات
        """
        return [s for s in self.shots if s.difficulty.value == difficulty]
    
    def get_shots_by_rails(self, rails: int) -> List[Shot]:
        """
        الحصول على التسديقات حسب عدد الجدران
        
        Args:
            rails: عدد الجدران (1-4)
        
        Returns:
            قائمة التسديقات
        """
        return [s for s in self.shots if s.rails == rails]
    
    def get_statistics(self) -> Dict:
        """
        الحصول على الإحصائيات الكاملة
        
        Returns:
            قاموس بالإحصائيات
        """
        return self.statistics.to_dict()
    
    def save_to_storage(self) -> None:
        """حفظ البيانات في التخزين المحلي"""
        try:
            # حفظ التسديقات
            shots_data = [s.to_dict() for s in self.shots]
            with open(self.shots_file, 'w', encoding='utf-8') as f:
                json.dump(shots_data, f, ensure_ascii=False, indent=2)
            
            # حفظ الإحصائيات
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.statistics.to_dict(), f, ensure_ascii=False, indent=2)
            
            logger.debug("✅ تم حفظ البيانات")
        except Exception as e:
            logger.error(f"❌ خطأ في حفظ البيانات: {e}")
            raise
    
    def load_from_storage(self) -> None:
        """تحميل البيانات من التخزين المحلي"""
        try:
            # تحميل التسديقات
            if self.shots_file.exists():
                with open(self.shots_file, 'r', encoding='utf-8') as f:
                    try:
                        shots_data = json.load(f)
                        self.shots = [Shot.from_dict(s) for s in shots_data]
                        logger.info(f"✅ تم تحميل {len(self.shots)} تسديقة")
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️ خطأ في قراءة ملف التسديقات: {e}")
                        self.shots = []
            
            # تحميل الإحصائيات
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    try:
                        stats_data = json.load(f)
                        logger.info("✅ تم تحميل الإحصائيات")
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️ خطأ في قراءة ملف الإحصائيات: {e}")
        except Exception as e:
            logger.error(f"❌ خطأ في تحميل البيانات: {e}")
