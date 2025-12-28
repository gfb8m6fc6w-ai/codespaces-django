/**
 * 🎯 محرك البلياردو الموحد (Billiards Engine)
 * 
 * هذا الملف يجمع كل أنظمة البلياردو في نظام واحد متكامل
 * يوفر واجهة موحدة للوصول لكل الميزات
 * 
 * @version 1.0.0
 * @author 5A System Pro
 */

class BilliardsEngine {
    /**
     * إنشاء محرك البلياردو الموحد
     */
    constructor() {
        console.log('🚀 تهيئة محرك البلياردو الموحد...');
        
        // التأكد من وجود الأنظمة الفرعية
        this.validateDependencies();
        
        // إنشاء الأنظمة الفرعية
        this.railSystem = new RailPositionsSystem();
        this.database = new BilliardsDatabase('billiardsEngine');
        
        // إذا كانت الأنظمة الهندسية موجودة
        if (typeof GeometryCalculator !== 'undefined') {
            this.geometryCalculator = new GeometryCalculator();
        }
        if (typeof ValidationEngine !== 'undefined') {
            this.validationEngine = new ValidationEngine();
        }
        if (typeof PerformanceOptimizer !== 'undefined') {
            this.performanceOptimizer = new PerformanceOptimizer();
        }
        
        // حالة التطبيق الحالية
        this.state = {
            currentMode: 'calculator', // calculator | dashboard | editor
            currentShot: null,
            filters: {},
            selectedMeasurement: null,
            darkMode: localStorage.getItem('darkMode') === 'true'
        };
        
        // الإحصائيات الكلية
        this.stats = {
            totalMeasurements: this.database.getStatistics().total,
            totalCalculations: 0,
            sessionStart: Date.now()
        };
        
        console.log('✅ محرك البلياردو جاهز للاستخدام');
    }

    /**
     * التحقق من وجود الأنظمة المطلوبة
     */
    validateDependencies() {
        const required = ['RailPositionsSystem', 'BilliardsDatabase'];
        const optional = ['GeometryCalculator', 'ValidationEngine', 'PerformanceOptimizer', 'ShotPathCalculator'];
        
        const missing = required.filter(dep => typeof window[dep] === 'undefined');
        
        if (missing.length > 0) {
            throw new Error(`❌ ملفات مطلوبة غير موجودة: ${missing.join(', ')}`);
        }
        
        optional.forEach(dep => {
            if (typeof window[dep] === 'undefined') {
                console.warn(`⚠️ ملف اختياري غير موجود: ${dep}`);
            }
        });
    }

    // ==========================================
    // 📊 عمليات الحساب
    // ==========================================

    /**
     * حساب قياس العصا
     * Target + WhiteBall = Cue
     */
    calculateCue(target, whiteBall) {
        const cue = parseFloat((target + whiteBall).toFixed(1));
        this.stats.totalCalculations++;
        return cue;
    }

    /**
     * حساب درجة الصعوبة
     */
    calculateDifficulty(rails, targetDistance, whiteBallDistance) {
        let difficulty = 30; // القاعدة
        
        // زيادة حسب عدد الجدران
        difficulty += (rails - 1) * 20;
        
        // زيادة حسب المسافة
        const maxDistance = 8;
        const distanceFactor = (Math.max(targetDistance, whiteBallDistance) / maxDistance) * 20;
        difficulty += distanceFactor;
        
        return Math.min(100, Math.max(0, difficulty));
    }

    /**
     * التحقق من صحة القياس
     */
    validateMeasurement(target, whiteBall, cue) {
        const expectedCue = this.calculateCue(target, whiteBall);
        const error = Math.abs(cue - expectedCue);
        const isCorrect = error <= 0.1;
        
        return {
            isCorrect,
            expectedCue,
            error: parseFloat(error.toFixed(2)),
            percentage: ((1 - (error / expectedCue)) * 100).toFixed(1)
        };
    }

    // ==========================================
    // 💾 عمليات إدارة البيانات
    // ==========================================

    /**
     * إضافة قياس جديد
     */
    addMeasurement(data) {
        // التحقق من البيانات
        if (!this.validationEngine) {
            if (!data.rails || !data.target || !data.whiteBall || !data.cue) {
                throw new Error('البيانات المطلوبة ناقصة');
            }
        }
        
        const measurement = this.database.addMeasurement(data);
        this.stats.totalMeasurements++;
        
        // إطلاق حدث لتحديث الواجهات
        this.dispatchEvent('measurementAdded', measurement);
        
        return measurement;
    }

    /**
     * تحديث قياس موجود
     */
    updateMeasurement(id, data) {
        const measurement = this.database.updateMeasurement(id, data);
        
        if (measurement) {
            this.dispatchEvent('measurementUpdated', measurement);
        }
        
        return measurement;
    }

    /**
     * حذف قياس
     */
    deleteMeasurement(id) {
        const result = this.database.deleteMeasurement(id);
        
        if (result) {
            this.stats.totalMeasurements--;
            this.dispatchEvent('measurementDeleted', { id });
        }
        
        return result;
    }

    /**
     * الحصول على جميع القياسات
     */
    getAllMeasurements() {
        return this.database.measurements;
    }

    /**
     * البحث في القياسات
     */
    searchMeasurements(query) {
        return this.database.search(query);
    }

    /**
     * فلترة القياسات
     */
    filterMeasurements(railsFilter = '', searchQuery = '') {
        return this.database.filter(railsFilter, searchQuery);
    }

    // ==========================================
    // 📈 الإحصائيات والتحليلات
    // ==========================================

    /**
     * الحصول على الإحصائيات الأساسية
     */
    getBasicStatistics() {
        return this.database.getStatistics();
    }

    /**
     * الحصول على الإحصائيات المتقدمة
     */
    getAdvancedStatistics() {
        return this.database.getAdvancedStats();
    }

    /**
     * الحصول على إحصائيات الجلسة الحالية
     */
    getSessionStatistics() {
        const sessionDuration = Date.now() - this.stats.sessionStart;
        
        return {
            totalMeasurements: this.stats.totalMeasurements,
            totalCalculations: this.stats.totalCalculations,
            sessionDuration: `${Math.floor(sessionDuration / 60000)} دقيقة`,
            durationMs: sessionDuration,
            avgCalculationsPerMinute: (
                (this.stats.totalCalculations / (sessionDuration / 60000)) || 0
            ).toFixed(2)
        };
    }

    // ==========================================
    // 🎨 عمليات الواجهة
    // ==========================================

    /**
     * تبديل وضع الليل
     */
    toggleDarkMode() {
        this.state.darkMode = !this.state.darkMode;
        localStorage.setItem('darkMode', this.state.darkMode);
        this.dispatchEvent('darkModeToggled', { darkMode: this.state.darkMode });
        return this.state.darkMode;
    }

    /**
     * تعيين الوضع الحالي
     */
    setMode(mode) {
        if (['calculator', 'dashboard', 'editor'].includes(mode)) {
            this.state.currentMode = mode;
            this.dispatchEvent('modeChanged', { mode });
            return true;
        }
        return false;
    }

    /**
     * الحصول على الوضع الحالي
     */
    getMode() {
        return this.state.currentMode;
    }

    // ==========================================
    // 💾 عمليات التخزين والتصدير
    // ==========================================

    /**
     * تصدير البيانات إلى JSON
     */
    exportToJSON() {
        const data = {
            version: '1.0.0',
            exportDate: new Date().toISOString(),
            measurements: this.database.export(),
            statistics: this.getAdvancedStatistics()
        };
        
        return JSON.stringify(data, null, 2);
    }

    /**
     * تصدير البيانات إلى CSV
     */
    exportToCSV() {
        const measurements = this.database.measurements;
        
        if (measurements.length === 0) {
            return 'لا توجد بيانات للتصدير';
        }
        
        // رؤوس الأعمدة
        const headers = ['التاريخ', 'الوقت', 'الجدران', 'التصويب', 'البيضا', 'العصا المتوقع', 'العصا الفعلي', 'الحالة', 'الملاحظات'];
        
        // البيانات
        const rows = measurements.map(m => [
            m.date,
            m.time,
            m.rails,
            m.target,
            m.whiteBall,
            m.expectedCue,
            m.cue,
            m.isCorrect ? 'صحيح' : 'غير صحيح',
            m.notes
        ]);
        
        // دمج الرؤوس والبيانات
        const csv = [headers, ...rows]
            .map(row => row.map(cell => `"${cell}"`).join(','))
            .join('\n');
        
        return csv;
    }

    /**
     * استيراد البيانات من JSON
     */
    importFromJSON(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            
            if (!data.measurements || !Array.isArray(data.measurements)) {
                throw new Error('صيغة JSON غير صحيحة');
            }
            
            this.database.import(data.measurements);
            this.stats.totalMeasurements = this.database.getStatistics().total;
            this.dispatchEvent('dataImported', { count: data.measurements.length });
            
            return { success: true, count: data.measurements.length };
        } catch (error) {
            console.error('❌ خطأ في الاستيراد:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * مسح جميع البيانات
     */
    clearAllData() {
        if (confirm('هل أنت متأكد من رغبتك في حذف جميع البيانات؟ هذا الإجراء لا يمكن التراجع عنه!')) {
            this.database.measurements = [];
            this.database.save();
            this.stats.totalMeasurements = 0;
            this.dispatchEvent('dataCleared', {});
            return true;
        }
        return false;
    }

    // ==========================================
    // 🔌 نظام الأحداث
    // ==========================================

    /**
     * إطلاق حدث مخصص
     */
    dispatchEvent(eventName, detail) {
        const event = new CustomEvent(`billiards:${eventName}`, { detail });
        window.dispatchEvent(event);
    }

    /**
     * الاستماع لحدث
     */
    addEventListener(eventName, callback) {
        window.addEventListener(`billiards:${eventName}`, (event) => {
            callback(event.detail);
        });
    }

    // ==========================================
    // 📱 عمليات الأجهزة المحمولة
    // ==========================================

    /**
     * التحقق من أن التطبيق محفوظ
     */
    isInstalled() {
        return window.navigator.standalone === true || 
               window.matchMedia('(display-mode: standalone)').matches;
    }

    /**
     * الحصول على معلومات الجهاز
     */
    getDeviceInfo() {
        return {
            isInstalled: this.isInstalled(),
            isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
            isTablet: /iPad|Android/i.test(navigator.userAgent),
            browser: this.detectBrowser(),
            platform: navigator.platform,
            userAgent: navigator.userAgent
        };
    }

    /**
     * اكتشاف المتصفح
     */
    detectBrowser() {
        const ua = navigator.userAgent;
        if (ua.indexOf('Firefox') > -1) return 'Firefox';
        if (ua.indexOf('Chrome') > -1) return 'Chrome';
        if (ua.indexOf('Safari') > -1) return 'Safari';
        if (ua.indexOf('Edge') > -1) return 'Edge';
        return 'Unknown';
    }

    // ==========================================
    // 🔧 عمليات الصيانة والتصحيح
    // ==========================================

    /**
     * تشخيص صحة النظام
     */
    diagnose() {
        const diagnosis = {
            timestamp: new Date().toISOString(),
            engineVersion: '1.0.0',
            systems: {
                railSystem: this.railSystem ? '✅' : '❌',
                database: this.database ? '✅' : '❌',
                geometryCalculator: this.geometryCalculator ? '✅' : '⚠️',
                validationEngine: this.validationEngine ? '✅' : '⚠️',
                performanceOptimizer: this.performanceOptimizer ? '✅' : '⚠️'
            },
            data: {
                totalMeasurements: this.stats.totalMeasurements,
                lastMeasurement: this.database.measurements[0] || null,
                storageUsed: this.estimateStorageUsage()
            },
            state: {
                currentMode: this.state.currentMode,
                darkMode: this.state.darkMode
            }
        };
        
        console.table(diagnosis);
        return diagnosis;
    }

    /**
     * تقدير استخدام التخزين
     */
    estimateStorageUsage() {
        const data = JSON.stringify(this.database.measurements);
        const bytes = new Blob([data]).size;
        
        return {
            bytes,
            KB: (bytes / 1024).toFixed(2),
            MB: (bytes / (1024 * 1024)).toFixed(2)
        };
    }

    /**
     * إعادة تعيين المحرك
     */
    reset() {
        if (confirm('هل تريد إعادة تعيين المحرك؟')) {
            this.state = {
                currentMode: 'calculator',
                currentShot: null,
                filters: {},
                selectedMeasurement: null,
                darkMode: false
            };
            this.stats = {
                totalMeasurements: this.database.getStatistics().total,
                totalCalculations: 0,
                sessionStart: Date.now()
            };
            this.dispatchEvent('engineReset', {});
            return true;
        }
        return false;
    }

    // ==========================================
    // 📚 المساعدة والتوثيق
    // ==========================================

    /**
     * الحصول على معلومات المحرك
     */
    getInfo() {
        return {
            name: 'BilliardsEngine',
            version: '1.0.0',
            description: 'محرك البلياردو الموحد',
            author: '5A System Pro',
            license: 'MIT',
            features: [
                'حساب قياسات البلياردو',
                'إدارة قاعدة البيانات',
                'الإحصائيات والتحليلات',
                'التصدير والاستيراد',
                'نظام الأحداث',
                'التشخيص والصيانة'
            ]
        };
    }

    /**
     * الحصول على قائمة الطرق المتاحة
     */
    getAvailableMethods() {
        return Object.getOwnPropertyNames(Object.getPrototypeOf(this))
            .filter(method => method !== 'constructor' && typeof this[method] === 'function')
            .map(method => ({
                name: method,
                description: this[method].description || 'لا توجد وصف'
            }));
    }
}

// إنشاء نسخة عامة من المحرك
let billiardsEngine = null;

/**
 * تهيئة محرك البلياردو
 */
function initializeBilliardsEngine() {
    try {
        billiardsEngine = new BilliardsEngine();
        window.billiards = billiardsEngine; // جعله متاحاً عالمياً
        console.log('🎯 محرك البلياردو الموحد جاهز!');
        return billiardsEngine;
    } catch (error) {
        console.error('❌ فشل إنشاء محرك البلياردو:', error);
        return null;
    }
}

// محاولة التهيئة تلقائياً عند تحميل الملف
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeBilliardsEngine);
} else {
    initializeBilliardsEngine();
}
