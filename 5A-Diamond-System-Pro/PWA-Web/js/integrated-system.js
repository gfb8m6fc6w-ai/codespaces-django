/**
 * 🎯 النظام المتكامل للبلياردو
 * مدير كامل يجمع جميع المكونات
 */

class BilliardsSystem {
    constructor() {
        this.storage = new StorageManager('billiards-system');
        this.backups = new BackupManager();
        this.theme = new ThemeManager();
        this.shots = [];
        this.settings = {};
        
        this.init();
    }

    init() {
        console.log('🚀 جاري تهيئة نظام البلياردو المتكامل...');
        
        // تطبيق الموضوع
        this.theme.applyTheme();
        
        // تحميل البيانات المحفوظة
        this.loadData();
        
        // التحقق من التحديثات
        UpdateManager.checkForUpdates();
        
        // إضافة مستمعي الأحداث
        this.setupEventListeners();
        
        console.log('✅ تم تهيئة النظام بنجاح');
    }

    // ==================== إدارة البيانات ====================
    
    addShot(shot) {
        shot.id = Date.now() + Math.random().toString(36).substr(2, 9);
        shot.timestamp = new Date().toISOString();
        this.shots.unshift(shot);
        this.saveData();
        NotificationManager.show('✅ تم حفظ التسديدة', 'success');
        return shot;
    }

    deleteShot(shotId) {
        const index = this.shots.findIndex(s => s.id === shotId);
        if (index !== -1) {
            this.shots.splice(index, 1);
            this.saveData();
            NotificationManager.show('✅ تم حذف التسديدة', 'success');
            return true;
        }
        return false;
    }

    updateShot(shotId, updates) {
        const shot = this.shots.find(s => s.id === shotId);
        if (shot) {
            Object.assign(shot, updates);
            shot.updatedAt = new Date().toISOString();
            this.saveData();
            NotificationManager.show('✅ تم تحديث التسديدة', 'success');
            return shot;
        }
        return null;
    }

    getShot(shotId) {
        return this.shots.find(s => s.id === shotId);
    }

    getAllShots() {
        return [...this.shots];
    }

    // ==================== البحث والتصفية ====================
    
    searchShots(query) {
        return this.shots.filter(shot => {
            const searchStr = JSON.stringify(shot).toLowerCase();
            return searchStr.includes(query.toLowerCase());
        });
    }

    filterShotsByRails(rails) {
        return this.shots.filter(shot => shot.rails === parseInt(rails));
    }

    filterShotsByDateRange(startDate, endDate) {
        return this.shots.filter(shot => {
            const shotDate = new Date(shot.timestamp);
            return shotDate >= startDate && shotDate <= endDate;
        });
    }

    // ==================== الإحصائيات ====================
    
    getStatistics() {
        if (this.shots.length === 0) {
            return {
                total: 0,
                successful: 0,
                failed: 0,
                successRate: 0,
                avgSuccess: 0,
                byRails: {},
                bestShot: null,
                worstShot: null
            };
        }

        const successful = this.shots.filter(s => s.success).length;
        const failed = this.shots.length - successful;
        
        const byRails = {};
        for (let i = 1; i <= 4; i++) {
            byRails[i] = this.shots.filter(s => s.rails === i).length;
        }

        const successRates = this.shots
            .filter(s => s.successRate !== undefined)
            .map(s => s.successRate);
        
        const avgSuccess = successRates.length > 0 
            ? successRates.reduce((a, b) => a + b, 0) / successRates.length 
            : 0;

        const bestShot = this.shots.reduce((max, shot) => {
            const shotRate = shot.successRate || 0;
            const maxRate = max.successRate || 0;
            return shotRate > maxRate ? shot : max;
        });

        const worstShot = this.shots.reduce((min, shot) => {
            const shotRate = shot.successRate || 0;
            const minRate = min.successRate || 0;
            return shotRate < minRate ? shot : min;
        });

        return {
            total: this.shots.length,
            successful: successful,
            failed: failed,
            successRate: ((successful / this.shots.length) * 100).toFixed(2),
            avgSuccess: avgSuccess.toFixed(2),
            byRails: byRails,
            bestShot: bestShot,
            worstShot: worstShot
        };
    }

    // ==================== النسخ الاحتياطية ====================
    
    createBackup() {
        const backup = this.backups.createBackup({
            shots: this.shots,
            settings: this.settings,
            timestamp: new Date().toISOString()
        });
        NotificationManager.show('✅ تم إنشاء نسخة احتياطية', 'success');
        return backup;
    }

    restoreBackup(backupId) {
        const data = this.backups.restoreBackup(backupId);
        if (data) {
            this.shots = data.shots || [];
            this.settings = data.settings || {};
            this.saveData();
            NotificationManager.show('✅ تم استعادة النسخة الاحتياطية', 'success');
            return true;
        }
        NotificationManager.show('❌ فشل استعادة النسخة الاحتياطية', 'error');
        return false;
    }

    listBackups() {
        return this.backups.listBackups();
    }

    // ==================== التصدير والاستيراد ====================
    
    exportData() {
        const data = {
            version: '3.0.0',
            exportDate: new Date().toISOString(),
            shots: this.shots,
            settings: this.settings,
            statistics: this.getStatistics()
        };
        ExportImportManager.export(data, 'billiards-data.json');
        NotificationManager.show('✅ تم تصدير البيانات', 'success');
    }

    importData(file) {
        ExportImportManager.import(file, (data) => {
            this.shots = data.shots || [];
            this.settings = data.settings || {};
            this.saveData();
        }, (error) => {
            console.error('❌ خطأ في الاستيراد:', error);
        });
    }

    // ==================== الحفظ والتحميل ====================
    
    saveData() {
        this.storage.save({
            shots: this.shots,
            settings: this.settings
        });
    }

    loadData() {
        const data = this.storage.load();
        if (data) {
            this.shots = data.shots || [];
            this.settings = data.settings || {};
        }
    }

    clearAllData() {
        if (confirm('⚠️ هل أنت متأكد من حذف جميع البيانات؟')) {
            this.shots = [];
            this.settings = {};
            this.storage.clear();
            NotificationManager.show('✅ تم مسح جميع البيانات', 'success');
            location.reload();
        }
    }

    // ==================== الإعدادات ====================
    
    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        this.saveData();
        NotificationManager.show('✅ تم تحديث الإعدادات', 'success');
    }

    getSettings() {
        return { ...this.settings };
    }

    resetSettings() {
        this.settings = {};
        this.saveData();
        NotificationManager.show('✅ تم إعادة تعيين الإعدادات', 'success');
    }

    // ==================== مستمعي الأحداث ====================
    
    setupEventListeners() {
        // تحديث البيانات عند تغيير نافذة أخرى
        window.addEventListener('storage', (e) => {
            if (e.key && e.key.startsWith(STORAGE_KEY)) {
                this.loadData();
                NotificationManager.show('🔄 تم تحديث البيانات من نافذة أخرى', 'info');
            }
        });

        // حفظ البيانات قبل إغلاق الصفحة
        window.addEventListener('beforeunload', () => {
            this.createBackup();
        });

        // معالجة الاتصال بالإنترنت
        window.addEventListener('online', () => {
            NotificationManager.show('✅ تم استعادة الاتصال بالإنترنت', 'success');
        });

        window.addEventListener('offline', () => {
            NotificationManager.show('⚠️ فقدت الاتصال بالإنترنت', 'warning');
        });
    }

    // ==================== الحسابات ====================
    
    calculateSuccessRate(angle, power, distance, difficulty = 2) {
        // تأثير الزاوية
        const angleFactor = 100 - (Math.abs(angle) * 0.5);
        
        // تأثير القوة
        let powerFactor;
        if (power >= 40 && power <= 80) {
            powerFactor = 100;
        } else if (power < 40) {
            powerFactor = 60 + (power - 20) * 1;
        } else {
            powerFactor = 100 - (power - 80) * 1;
        }

        // تأثير المسافة
        let distanceFactor;
        if (distance <= 50) {
            distanceFactor = 100;
        } else if (distance <= 200) {
            distanceFactor = 100 - (distance - 50) * 0.25;
        } else {
            distanceFactor = 100 - (distance - 200) * 0.1;
        }

        // حساب النسبة النهائية
        const baseRate = (angleFactor * 0.25) + (powerFactor * 0.25) + (distanceFactor * 0.25) + (distance > 0 ? 25 : 0);
        
        // تطبيق معامل الصعوبة
        const difficultyFactor = 1 - (difficulty * 0.1);
        const finalRate = baseRate * difficultyFactor;

        return Math.max(0, Math.min(100, finalRate));
    }

    // ==================== معلومات النظام ====================
    
    getSystemInfo() {
        return {
            version: '3.0.0',
            storageKey: STORAGE_KEY,
            totalShots: this.shots.length,
            dataSize: JSON.stringify({
                shots: this.shots,
                settings: this.settings
            }).length,
            lastBackup: this.listBackups()[0]?.timestamp || 'لا توجد',
            theme: this.theme.currentTheme,
            online: navigator.onLine
        };
    }
}

// ==================== إنشاء النسق العام ====================
let billiardSystem;

document.addEventListener('DOMContentLoaded', () => {
    billiardSystem = new BilliardsSystem();
    window.billiardSystem = billiardSystem; // جعله متاحاً عالمياً
    console.log('🎉 نظام البلياردو المتكامل جاهز للاستخدام');
});

// ==================== تصدير ====================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BilliardsSystem;
}
