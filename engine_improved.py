"""
محرك البلياردو الرئيسي - محسّن بـ Logging والأداء
"""

from typing import List, Optional, Dict
from .calculator import ShotCalculator
from .rail_system import RailPositionsSystem
from ..models.shot import Shot, ShotStatistics
from ..models.statistics import Statistics
import json
from pathlib import Path
from datetime import datetime
import logging

# إعداد Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BilliardsEngine:
    """
    محرك البلياردو الرئيسي - محسّن للأداء
    يجمع جميع الأنظمة الفرعية مع معالجة أخطاء قوية
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        تهيئة محرك البلياردو
        
        Args:
            data_dir: مسار مجلد البيانات (اختياري)
        """
        logger.info("جاري تهيئة محرك البلياردو...")
        
        try:
            self.calculator = ShotCalculator()
            self.rail_system = RailPositionsSystem()
            self.shots: List[Shot] = []
            self.statistics = Statistics()
            
            # مسار البيانات
            if data_dir:
                self.data_dir = Path(data_dir)
            else:
                self.data_dir = Path.home() / ".billiards_pro"
            
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.shots_file = self.data_dir / "shots.json"
            self.stats_file = self.data_dir / "statistics.json"
            
            # تحميل البيانات الموجودة
            self.load_from_storage()
            logger.info("✅ تم تهيئة محرك البلياردو بنجاح")
        
        except Exception as e:
            logger.error(f"❌ خطأ في تهيئة المحرك: {e}")
            raise
    
    def calculate_shot(self, rails: int, cue_position: float, white_ball: float,
                      target: float, pocket: int) -> Shot:
        """
        حساب وإنشاء تسديقة جديدة
        
        Args:
            rails: عدد الجدران (1-4)
            cue_position: موضع العصا
            white_ball: موضع الكرة البيضاء
            target: موضع الهدف
            pocket: موضع الجيب المستهدف
        
        Returns:
            كائن التسديقة المحسوب
        
        Raises:
            ValueError: إذا كانت المعاملات غير صحيحة
        """
        try:
            # التحقق من المعاملات
            if not (1 <= rails <= 4):
                raise ValueError(f"عدد الجدران يجب أن يكون بين 1 و 4، الحصول على: {rails}")
            if not (0 <= cue_position <= 10):
                raise ValueError(f"موضع العصا يجب أن يكون بين 0 و 10")
            if not (0 <= white_ball <= 10):
                raise ValueError(f"موضع الكرة البيضاء يجب أن يكون بين 0 و 10")
            if not (0 <= target <= 10):
                raise ValueError(f"موضع الهدف يجب أن يكون بين 0 و 10")
            if not (0 <= pocket <= 5):
                raise ValueError(f"موضع الجيب يجب أن يكون بين 0 و 5")
            
            shot = self.calculator.create_shot(rails, cue_position, white_ball, target, pocket)
            self.shots.append(shot)
            self.statistics.total_calculations += 1
            
            logger.info(f"✅ تم حساب تسديقة: جدران={rails}, صعوبة={shot.difficulty.value}")
            return shot
        
        except ValueError as e:
            logger.warning(f"⚠️ خطأ في المعاملات: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ خطأ غير متوقع عند حساب التسديقة: {e}")
            raise
    
    def record_execution(self, shot: Shot, successful: bool) -> None:
        """
        تسجيل نتيجة تنفيذ التسديقة
        
        Args:
            shot: التسديقة
            successful: هل كانت ناجحة؟
        """
        try:
            if shot not in self.shots:
                raise ValueError("التسديقة لم تكن من قائمة التسديقات")
            
            shot.executed = True
            self.statistics.total_shots_attempted += 1
            
            if successful:
                self.statistics.total_shots_successful += 1
                logger.info(f"✅ تسديقة ناجحة (معدل النجاح: {self.statistics.success_rate:.1f}%)")
            else:
                logger.info(f"❌ تسديقة فاشلة")
            
            self.save_to_storage()
        
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
        try:
            shots = [s for s in self.shots if s.difficulty.value == difficulty]
            logger.info(f"تم البحث: {len(shots)} تسديقة بمستوى صعوبة '{difficulty}'")
            return shots
        
        except Exception as e:
            logger.error(f"❌ خطأ في البحث حسب الصعوبة: {e}")
            raise
    
    def get_shots_by_rails(self, rails: int) -> List[Shot]:
        """
        الحصول على التسديقات حسب عدد الجدران
        
        Args:
            rails: عدد الجدران
        
        Returns:
            قائمة التسديقات
        """
        try:
            if not (1 <= rails <= 4):
                raise ValueError(f"عدد الجدران غير صحيح: {rails}")
            
            shots = [s for s in self.shots if s.rails == rails]
            logger.info(f"تم البحث: {len(shots)} تسديقة بـ {rails} جدران")
            return shots
        
        except Exception as e:
            logger.error(f"❌ خطأ في البحث حسب الجدران: {e}")
            raise
    
    def get_statistics(self) -> Dict:
        """
        الحصول على الإحصائيات الكاملة
        
        Returns:
            قاموس بالإحصائيات
        """
        try:
            stats = self.statistics.to_dict()
            logger.debug("تم الحصول على الإحصائيات")
            return stats
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على الإحصائيات: {e}")
            raise
    
    def save_to_storage(self) -> None:
        """
        حفظ البيانات في التخزين
        مع معالجة أخطاء قوية
        """
        try:
            # حفظ التسديقات
            shots_data = [s.to_dict() for s in self.shots]
            with open(self.shots_file, 'w', encoding='utf-8') as f:
                json.dump(shots_data, f, ensure_ascii=False, indent=2)
            
            # حفظ الإحصائيات
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.statistics.to_dict(), f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ تم حفظ {len(self.shots)} تسديقة")
        
        except IOError as e:
            logger.error(f"❌ خطأ في الكتابة إلى الملف: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ خطأ غير متوقع عند الحفظ: {e}")
            raise
    
    def load_from_storage(self) -> None:
        """
        تحميل البيانات من التخزين
        مع معالجة أخطاء قوية
        """
        try:
            # تحميل التسديقات
            if self.shots_file.exists():
                with open(self.shots_file, 'r', encoding='utf-8') as f:
                    try:
                        shots_data = json.load(f)
                        self.shots = [Shot.from_dict(s) for s in shots_data]
                        logger.info(f"✅ تم تحميل {len(self.shots)} تسديقة")
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️ ملف التسديقات تالف: {e}")
                        self.shots = []
            
            # تحميل الإحصائيات
            if self.stats_file.exists():
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    try:
                        stats_data = json.load(f)
                        logger.info("✅ تم تحميل الإحصائيات")
                    except json.JSONDecodeError as e:
                        logger.warning(f"⚠️ ملف الإحصائيات تالف: {e}")
        
        except Exception as e:
            logger.error(f"❌ خطأ في التحميل: {e}")
            raise
    
    def get_performance_stats(self) -> Dict:
        """
        الحصول على إحصائيات الأداء
        
        Returns:
            قاموس بإحصائيات الأداء
        """
        try:
            return {
                'total_shots': len(self.shots),
                'total_calculations': self.statistics.total_calculations,
                'success_rate': self.statistics.success_rate,
                'cache_size': len(self.calculator._difficulty_cache),
                'total_memory_usage': f"{self.statistics.total_shots_attempted} shots"
            }
        
        except Exception as e:
            logger.error(f"❌ خطأ في الحصول على إحصائيات الأداء: {e}")
            raise
    
    def clear_old_data(self, days: int = 30) -> int:
        """
        حذف البيانات القديمة
        
        Args:
            days: عدد الأيام (البيانات الأقدم من هذا سيتم حذفها)
        
        Returns:
            عدد التسديقات المحذوفة
        """
        try:
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            initial_count = len(self.shots)
            
            self.shots = [
                s for s in self.shots
                if s.timestamp.timestamp() > cutoff_date
            ]
            
            deleted_count = initial_count - len(self.shots)
            
            if deleted_count > 0:
                self.save_to_storage()
                logger.info(f"✅ تم حذف {deleted_count} تسديقة قديمة")
            
            return deleted_count
        
        except Exception as e:
            logger.error(f"❌ خطأ في حذف البيانات القديمة: {e}")
            raise
