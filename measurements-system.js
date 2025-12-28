// 📁 measurements-system.js
// نظام متقدم لإدارة قياسات البلياردو

/**
 * فئة لإدارة قياسات البلياردو
 */
class BilliardsDatabase {
    constructor(storageKey = 'billiardsDB') {
        this.storageKey = storageKey;
        this.measurements = [];
        this.load();
    }

    /**
     * إضافة قياسة جديدة
     */
    addMeasurement(data) {
        const measurement = {
            id: Date.now(),
            rails: parseInt(data.rails),
            whiteBall: parseFloat(data.whiteBall),
            target: parseFloat(data.target),
            cue: parseFloat(data.cue),
            notes: data.notes || '',
            date: new Date().toLocaleDateString('ar-SA'),
            time: new Date().toLocaleTimeString('ar-SA'),
            timestamp: Date.now()
        };

        // التحقق من المعادلة
        measurement.expectedCue = parseFloat((measurement.whiteBall + measurement.target).toFixed(1));
        measurement.isCorrect = Math.abs(measurement.cue - measurement.expectedCue) <= 0.1;
        measurement.error = parseFloat((measurement.cue - measurement.expectedCue).toFixed(2));

        this.measurements.unshift(measurement);
        this.save();
        return measurement;
    }

    /**
     * تحديث قياسة موجودة
     */
    updateMeasurement(id, data) {
        const index = this.measurements.findIndex(m => m.id === id);
        if (index !== -1) {
            const measurement = {
                ...this.measurements[index],
                rails: parseInt(data.rails),
                whiteBall: parseFloat(data.whiteBall),
                target: parseFloat(data.target),
                cue: parseFloat(data.cue),
                notes: data.notes || '',
                updatedDate: new Date().toLocaleDateString('ar-SA'),
                updatedTime: new Date().toLocaleTimeString('ar-SA')
            };

            measurement.expectedCue = parseFloat((measurement.whiteBall + measurement.target).toFixed(1));
            measurement.isCorrect = Math.abs(measurement.cue - measurement.expectedCue) <= 0.1;
            measurement.error = parseFloat((measurement.cue - measurement.expectedCue).toFixed(2));

            this.measurements[index] = measurement;
            this.save();
            return measurement;
        }
        return null;
    }

    /**
     * حذف قياسة
     */
    deleteMeasurement(id) {
        const index = this.measurements.findIndex(m => m.id === id);
        if (index !== -1) {
            this.measurements.splice(index, 1);
            this.save();
            return true;
        }
        return false;
    }

    /**
     * الحصول على جميع القياسات
     */
    getAll() {
        return this.measurements;
    }

    /**
     * الحصول على قياسات حسب عدد الجدران
     */
    getByRails(rails) {
        return this.measurements.filter(m => m.rails === rails);
    }

    /**
     * البحث في القياسات
     */
    search(query) {
        const lowerQuery = query.toLowerCase();
        return this.measurements.filter(m => 
            m.notes.toLowerCase().includes(lowerQuery) ||
            m.whiteBall.toString().includes(query) ||
            m.target.toString().includes(query) ||
            m.cue.toString().includes(query)
        );
    }

    /**
     * الحصول على إحصائيات
     */
    getStatistics() {
        const total = this.measurements.length;
        const byRails = {
            1: this.measurements.filter(m => m.rails === 1).length,
            2: this.measurements.filter(m => m.rails === 2).length,
            3: this.measurements.filter(m => m.rails === 3).length,
            4: this.measurements.filter(m => m.rails === 4).length
        };

        const correctCount = this.measurements.filter(m => m.isCorrect).length;
        const incorrectCount = total - correctCount;

        const avgError = total > 0 
            ? parseFloat((this.measurements.reduce((sum, m) => sum + Math.abs(m.error), 0) / total).toFixed(2))
            : 0;

        return {
            total,
            byRails,
            correctCount,
            incorrectCount,
            accuracyRate: total > 0 ? ((correctCount / total) * 100).toFixed(1) : 0,
            avgError,
            oldestEntry: total > 0 ? this.measurements[total - 1] : null,
            newestEntry: total > 0 ? this.measurements[0] : null
        };
    }

    /**
     * حفظ في localStorage
     */
    save() {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(this.measurements));
            return true;
        } catch (e) {
            console.error('خطأ في الحفظ:', e);
            return false;
        }
    }

    /**
     * تحميل من localStorage
     */
    load() {
        try {
            const data = localStorage.getItem(this.storageKey);
            this.measurements = data ? JSON.parse(data) : [];
            return true;
        } catch (e) {
            console.error('خطأ في التحميل:', e);
            this.measurements = [];
            return false;
        }
    }

    /**
     * تصدير البيانات
     */
    export() {
        return JSON.stringify(this.measurements, null, 2);
    }

    /**
     * استيراد البيانات
     */
    import(jsonData) {
        try {
            const data = JSON.parse(jsonData);
            if (Array.isArray(data)) {
                this.measurements = [...this.measurements, ...data];
                this.save();
                return true;
            }
            return false;
        } catch (e) {
            console.error('خطأ في الاستيراد:', e);
            return false;
        }
    }

    /**
     * حذف جميع البيانات
     */
    clear() {
        this.measurements = [];
        this.save();
    }

    /**
     * إحصائيات متقدمة
     */
    getAdvancedStats() {
        const stats = this.getStatistics();
        
        // أكثر مسافة استخدام
        const distanceFreq = {};
        this.measurements.forEach(m => {
            const distance = m.whiteBall + m.target;
            distanceFreq[distance] = (distanceFreq[distance] || 0) + 1;
        });

        const mostUsedDistance = Object.entries(distanceFreq).sort((a, b) => b[1] - a[1])[0];

        // أكثر موقع كرة بيضاء
        const whiteBallFreq = {};
        this.measurements.forEach(m => {
            whiteBallFreq[m.whiteBall] = (whiteBallFreq[m.whiteBall] || 0) + 1;
        });
        const mostUsedWhiteBall = Object.entries(whiteBallFreq).sort((a, b) => b[1] - a[1])[0];

        return {
            ...stats,
            mostUsedDistance: mostUsedDistance ? { distance: parseFloat(mostUsedDistance[0]), count: mostUsedDistance[1] } : null,
            mostUsedWhiteBall: mostUsedWhiteBall ? { position: parseFloat(mostUsedWhiteBall[0]), count: mostUsedWhiteBall[1] } : null
        };
    }

    /**
     * حساب الدقة لفترة محددة
     */
    getAccuracyForPeriod(days) {
        const cutoffDate = Date.now() - (days * 24 * 60 * 60 * 1000);
        const recent = this.measurements.filter(m => m.timestamp >= cutoffDate);
        
        if (recent.length === 0) return 0;
        
        const correct = recent.filter(m => m.isCorrect).length;
        return ((correct / recent.length) * 100).toFixed(1);
    }
}

// إنشاء مثيل عام
const billiardsDB = new BilliardsDatabase('billiardsDatabase');

// تصدير للاستخدام
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BilliardsDatabase;
}
