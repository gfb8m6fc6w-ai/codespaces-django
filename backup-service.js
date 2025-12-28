/**
 * 💾 خدمة النسخ الاحتياطي والاستعادة
 * 
 * توفر نسخ احتياطية تلقائية وسهولة استعادة البيانات
 */

class BackupService {
    constructor(interval = 3600000, maxBackups = 10) { // 1 ساعة، 10 نسخ أقصى
        this.interval = interval;
        this.maxBackups = maxBackups;
        this.backups = this.loadBackups();
        this.isAutoBackupEnabled = true;
        this.startAutoBackup();
    }

    /**
     * تحميل النسخ الاحتياطية من التخزين
     */
    loadBackups() {
        try {
            const stored = localStorage.getItem('backups');
            return stored ? JSON.parse(stored) : [];
        } catch (error) {
            console.error('❌ خطأ في تحميل النسخ الاحتياطية:', error);
            return [];
        }
    }

    /**
     * حفظ النسخ الاحتياطية في التخزين
     */
    saveBackups() {
        try {
            localStorage.setItem('backups', JSON.stringify(this.backups));
            return { success: true };
        } catch (error) {
            console.error('❌ خطأ في حفظ النسخ الاحتياطية:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * إنشاء نسخة احتياطية
     */
    createBackup(label = '') {
        try {
            const backup = {
                id: this.generateId(),
                label: label || `نسخة احتياطية - ${new Date().toLocaleString('ar-EG')}`,
                timestamp: new Date().toISOString(),
                date: new Date().toLocaleDateString('ar-EG'),
                time: new Date().toLocaleTimeString('ar-EG'),
                data: this.getAllData(),
                size: 0,
                version: '2.0.1'
            };

            // حساب حجم النسخة
            backup.size = new Blob([JSON.stringify(backup.data)]).size;

            this.backups.push(backup);

            // احتفظ بأحدث N نسخة فقط
            if (this.backups.length > this.maxBackups) {
                const removed = this.backups.shift();
                console.log(`🗑️ تم حذف النسخة القديمة: ${removed.label}`);
            }

            this.saveBackups();

            console.log(`✅ تم إنشاء نسخة احتياطية: ${backup.label}`);
            return backup;
        } catch (error) {
            console.error('❌ خطأ في إنشاء النسخة الاحتياطية:', error);
            throw error;
        }
    }

    /**
     * استعادة نسخة احتياطية
     */
    restoreBackup(backupId, confirm = true) {
        try {
            const backup = this.backups.find(b => b.id === backupId);

            if (!backup) {
                throw new Error('النسخة الاحتياطية غير موجودة');
            }

            // تحذير قبل الاستعادة
            if (confirm && !window.confirm(`هل أنت متأكد من استعادة النسخة: ${backup.label}?`)) {
                return { success: false, reason: 'تم الإلغاء من قبل المستخدم' };
            }

            // إنشاء نسخة احتياطية قبل الاستعادة
            this.createBackup('نسخة قبل الاستعادة');

            // استعادة البيانات
            this.restoreAllData(backup.data);

            console.log(`✅ تم استعادة النسخة: ${backup.label}`);
            return { success: true, backup };
        } catch (error) {
            console.error('❌ خطأ في استعادة النسخة:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * حذف نسخة احتياطية
     */
    deleteBackup(backupId) {
        const index = this.backups.findIndex(b => b.id === backupId);

        if (index === -1) {
            return { success: false, error: 'النسخة الاحتياطية غير موجودة' };
        }

        const deleted = this.backups.splice(index, 1)[0];
        this.saveBackups();

        console.log(`🗑️ تم حذف النسخة: ${deleted.label}`);
        return { success: true, deleted };
    }

    /**
     * حذف جميع النسخ الاحتياطية
     */
    deleteAllBackups(confirm = true) {
        if (confirm && !window.confirm('هل أنت متأكد من حذف جميع النسخ الاحتياطية؟')) {
            return { success: false };
        }

        const count = this.backups.length;
        this.backups = [];
        this.saveBackups();

        console.log(`🗑️ تم حذف ${count} نسخة احتياطية`);
        return { success: true, deleted: count };
    }

    /**
     * قائمة النسخ الاحتياطية
     */
    listBackups(limit = null) {
        let list = [...this.backups].reverse(); // أحدث أولاً

        if (limit) {
            list = list.slice(0, limit);
        }

        return list.map(b => ({
            id: b.id,
            label: b.label,
            timestamp: b.timestamp,
            date: b.date,
            time: b.time,
            size: (b.size / 1024).toFixed(2) + ' KB',
            version: b.version
        }));
    }

    /**
     * حجم جميع النسخ الاحتياطية
     */
    getTotalSize() {
        const total = this.backups.reduce((sum, b) => sum + (b.size || 0), 0);
        return {
            bytes: total,
            kb: (total / 1024).toFixed(2),
            mb: (total / 1024 / 1024).toFixed(2)
        };
    }

    /**
     * بدء النسخ الاحتياطية التلقائية
     */
    startAutoBackup() {
        if (this.autoBackupInterval) {
            clearInterval(this.autoBackupInterval);
        }

        this.autoBackupInterval = setInterval(() => {
            if (this.isAutoBackupEnabled) {
                this.createBackup('نسخة احتياطية تلقائية');
            }
        }, this.interval);

        console.log(`⏰ تم تفعيل النسخ الاحتياطي التلقائي كل ${this.interval / 60000} دقيقة`);
    }

    /**
     * إيقاف النسخ الاحتياطية التلقائية
     */
    stopAutoBackup() {
        if (this.autoBackupInterval) {
            clearInterval(this.autoBackupInterval);
        }
        this.isAutoBackupEnabled = false;
        console.log('⏸️ تم إيقاف النسخ الاحتياطي التلقائي');
    }

    /**
     * تفعيل/تعطيل النسخ التلقائية
     */
    toggleAutoBackup(enable) {
        this.isAutoBackupEnabled = enable;
        console.log(`${enable ? '✅' : '❌'} النسخ الاحتياطي التلقائي ${enable ? 'مفعّل' : 'معطّل'}`);
    }

    /**
     * مقارنة نسختين احتياطيتين
     */
    compareBackups(backupId1, backupId2) {
        const backup1 = this.backups.find(b => b.id === backupId1);
        const backup2 = this.backups.find(b => b.id === backupId2);

        if (!backup1 || !backup2) {
            return { error: 'نسخة واحدة أو كلاهما غير موجودة' };
        }

        return {
            backup1: { label: backup1.label, size: backup1.size, date: backup1.date },
            backup2: { label: backup2.label, size: backup2.size, date: backup2.date },
            sizeDifference: backup2.size - backup1.size,
            timeDifference: new Date(backup2.timestamp) - new Date(backup1.timestamp)
        };
    }

    /**
     * الحصول على إحصائيات النسخ
     */
    getStatistics() {
        const sizes = this.backups.map(b => b.size || 0);

        return {
            totalBackups: this.backups.length,
            totalSize: this.getTotalSize(),
            averageSize: sizes.length > 0 ? (sizes.reduce((a, b) => a + b) / sizes.length).toFixed(0) + ' B' : '0 B',
            oldestBackup: this.backups.length > 0 ? this.backups[0].date : 'لا توجد',
            newestBackup: this.backups.length > 0 ? this.backups[this.backups.length - 1].date : 'لا توجد',
            autoBackupEnabled: this.isAutoBackupEnabled,
            maxBackups: this.maxBackups
        };
    }

    /**
     * تصدير النسخة الاحتياطية كملف
     */
    exportBackup(backupId, format = 'json') {
        const backup = this.backups.find(b => b.id === backupId);

        if (!backup) {
            throw new Error('النسخة الاحتياطية غير موجودة');
        }

        const data = format === 'json'
            ? JSON.stringify(backup, null, 2)
            : this.backupToCSV(backup);

        const blob = new Blob([data], {
            type: format === 'json' ? 'application/json' : 'text/csv'
        });

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `backup-${backup.id}.${format === 'json' ? 'json' : 'csv'}`;
        a.click();
        URL.revokeObjectURL(url);

        return { success: true, file: `backup-${backup.id}.${format}` };
    }

    /**
     * تحويل النسخة إلى CSV
     */
    backupToCSV(backup) {
        let csv = `ID,التاريخ,الوقت,الحجم,الإصدار\n`;
        csv += `${backup.id},"${backup.date}","${backup.time}",${backup.size},"${backup.version}"\n`;
        return csv;
    }

    /**
     * استيراد نسخة احتياطية من ملف
     */
    importBackup(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = (e) => {
                try {
                    const imported = JSON.parse(e.target.result);

                    if (!imported.id || !imported.data) {
                        reject(new Error('تنسيق الملف غير صحيح'));
                        return;
                    }

                    // إضافة النسخة المستوردة
                    this.backups.push(imported);
                    this.saveBackups();

                    resolve({
                        success: true,
                        backup: imported,
                        message: `تم استيراد النسخة: ${imported.label}`
                    });
                } catch (error) {
                    reject(error);
                }
            };

            reader.onerror = () => reject(new Error('فشل قراءة الملف'));
            reader.readAsText(file);
        });
    }

    /**
     * إنشاء معرّف فريد
     */
    generateId() {
        return `backup_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * الحصول على جميع البيانات
     */
    getAllData() {
        return {
            measurements: StorageService.load('measurements', []),
            settings: StorageService.load('settings', {}),
            history: StorageService.load('history', []),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * استعادة جميع البيانات
     */
    restoreAllData(data) {
        StorageService.save('measurements', data.measurements || []);
        StorageService.save('settings', data.settings || {});
        StorageService.save('history', data.history || []);
    }

    /**
     * التحقق من صحة النسخة
     */
    validateBackup(backupId) {
        const backup = this.backups.find(b => b.id === backupId);

        if (!backup) {
            return { valid: false, error: 'النسخة غير موجودة' };
        }

        const checks = {
            hasId: !!backup.id,
            hasData: !!backup.data,
            hasTimestamp: !!backup.timestamp,
            isValidJSON: this.isValidJSON(backup.data),
            hasMeasurements: Array.isArray(backup.data.measurements),
            hasSettings: typeof backup.data.settings === 'object'
        };

        const valid = Object.values(checks).every(v => v);

        return { valid, checks };
    }

    /**
     * التحقق من صحة JSON
     */
    isValidJSON(obj) {
        try {
            JSON.stringify(obj);
            return true;
        } catch {
            return false;
        }
    }
}

// ==========================================
// الاستخدام
// ==========================================

const Backup = new BackupService();

/*

// إنشاء نسخة احتياطية يدوية
const backup = Backup.createBackup('النسخة قبل الحدث المهم');

// قائمة النسخ
console.log('📋 قائمة النسخ:', Backup.listBackups());

// الإحصائيات
console.log('📊 الإحصائيات:', Backup.getStatistics());

// استعادة نسخة
Backup.restoreBackup(backup.id);

// تصدير النسخة
Backup.exportBackup(backup.id);

// حذف نسخة
Backup.deleteBackup(backup.id);

*/
