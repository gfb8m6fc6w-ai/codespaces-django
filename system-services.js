/**
 * 🔧 خدمات النظام المركزية
 * 
 * مجموعة من الخدمات المركزية التي توفر وظائف موحدة
 * للتطبيق بأكمله
 */

// ==========================================
// 1️⃣ خدمة التخزين المركزي
// ==========================================

class StorageService {
    constructor() {
        this.storageKey = 'billiardsAppStorage';
        this.initStorage();
    }

    /**
     * تهيئة التخزين
     */
    initStorage() {
        if (!localStorage.getItem(this.storageKey)) {
            localStorage.setItem(this.storageKey, JSON.stringify({
                measurements: [],
                settings: {},
                history: []
            }));
        }
    }

    /**
     * حفظ البيانات
     */
    save(key, data) {
        try {
            const storage = JSON.parse(localStorage.getItem(this.storageKey));
            storage[key] = data;
            localStorage.setItem(this.storageKey, JSON.stringify(storage));
            return { success: true };
        } catch (error) {
            console.error('❌ خطأ في الحفظ:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * تحميل البيانات
     */
    load(key, defaultValue = null) {
        try {
            const storage = JSON.parse(localStorage.getItem(this.storageKey));
            return storage[key] || defaultValue;
        } catch (error) {
            console.error('❌ خطأ في التحميل:', error);
            return defaultValue;
        }
    }

    /**
     * حذف البيانات
     */
    delete(key) {
        try {
            const storage = JSON.parse(localStorage.getItem(this.storageKey));
            delete storage[key];
            localStorage.setItem(this.storageKey, JSON.stringify(storage));
            return { success: true };
        } catch (error) {
            console.error('❌ خطأ في الحذف:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * الحصول على جميع البيانات
     */
    getAll() {
        try {
            return JSON.parse(localStorage.getItem(this.storageKey));
        } catch (error) {
            console.error('❌ خطأ في الحصول على البيانات:', error);
            return null;
        }
    }

    /**
     * مسح كل شيء
     */
    clear() {
        try {
            localStorage.removeItem(this.storageKey);
            this.initStorage();
            return { success: true };
        } catch (error) {
            console.error('❌ خطأ في المسح:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * التحقق من حالة التخزين
     */
    getStatus() {
        const data = this.getAll();
        const used = JSON.stringify(data).length;
        const limit = 5 * 1024 * 1024; // 5MB
        
        return {
            used: used,
            limit: limit,
            percentage: ((used / limit) * 100).toFixed(2),
            available: limit - used,
            items: {
                measurements: (data.measurements || []).length,
                settings: Object.keys(data.settings || {}).length,
                history: (data.history || []).length
            }
        };
    }
}

// ==========================================
// 2️⃣ خدمة التصدير والاستيراد
// ==========================================

class ExportService {
    /**
     * تصدير إلى ملف JSON
     */
    static downloadJSON(data, filename = 'billiards-data.json') {
        const json = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        ExportService.downloadFile(blob, filename);
    }

    /**
     * تصدير إلى ملف CSV
     */
    static downloadCSV(data, filename = 'billiards-data.csv') {
        const csv = typeof data === 'string' ? data : ExportService.arrayToCSV(data);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        ExportService.downloadFile(blob, filename);
    }

    /**
     * تصدير إلى ملف Excel (يعمل كـ CSV محسّن)
     */
    static downloadExcel(data, filename = 'billiards-data.xlsx') {
        const csv = typeof data === 'string' ? data : ExportService.arrayToCSV(data);
        const blob = new Blob(['\ufeff' + csv], { type: 'application/vnd.ms-excel;charset=utf-8;' });
        ExportService.downloadFile(blob, filename);
    }

    /**
     * تحويل مصفوفة إلى CSV
     */
    static arrayToCSV(data) {
        if (!Array.isArray(data) || data.length === 0) {
            return '';
        }

        const headers = Object.keys(data[0]);
        const rows = data.map(obj =>
            headers.map(header =>
                `"${String(obj[header] || '').replace(/"/g, '""')}"`
            ).join(',')
        );

        return [headers.join(','), ...rows].join('\n');
    }

    /**
     * تحميل ملف من الجهاز
     */
    static uploadFile(fileInput) {
        return new Promise((resolve, reject) => {
            const file = fileInput.files[0];
            if (!file) {
                reject(new Error('لم يتم اختيار ملف'));
                return;
            }

            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const content = e.target.result;
                    
                    // محاولة فهم الملف كـ JSON أولاً
                    try {
                        const data = JSON.parse(content);
                        resolve({ type: 'json', data });
                    } catch {
                        // إذا فشل، افترض أنه CSV
                        resolve({ type: 'csv', data: content });
                    }
                } catch (error) {
                    reject(error);
                }
            };
            reader.onerror = () => reject(new Error('فشل قراءة الملف'));
            reader.readAsText(file);
        });
    }

    /**
     * تحميل ملف عام
     */
    static downloadFile(blob, filename) {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    /**
     * نسخ النص للحافظة
     */
    static copyToClipboard(text) {
        return navigator.clipboard.writeText(text).then(() => true).catch(() => false);
    }
}

// ==========================================
// 3️⃣ خدمة التحليلات
// ==========================================

class AnalyticsService {
    constructor() {
        this.events = [];
        this.startTime = Date.now();
    }

    /**
     * تسجيل حدث
     */
    trackEvent(eventName, data = {}) {
        this.events.push({
            name: eventName,
            timestamp: Date.now(),
            data
        });
        
        // احفظ آخر 100 حدث فقط
        if (this.events.length > 100) {
            this.events.shift();
        }
    }

    /**
     * الحصول على الأحداث
     */
    getEvents(filter = null) {
        if (!filter) return this.events;
        return this.events.filter(e => e.name === filter);
    }

    /**
     * الحصول على الإحصائيات
     */
    getStats() {
        const totalEvents = this.events.length;
        const eventTypes = {};
        
        this.events.forEach(e => {
            eventTypes[e.name] = (eventTypes[e.name] || 0) + 1;
        });
        
        return {
            totalEvents,
            eventTypes,
            sessionDuration: Date.now() - this.startTime,
            firstEvent: this.events[0] || null,
            lastEvent: this.events[this.events.length - 1] || null
        };
    }

    /**
     * مسح الأحداث
     */
    clear() {
        this.events = [];
        this.startTime = Date.now();
    }

    /**
     * تصدير الأحداث
     */
    export() {
        return {
            events: this.events,
            stats: this.getStats(),
            exportDate: new Date().toISOString()
        };
    }
}

// ==========================================
// 4️⃣ خدمة المزامنة والتنسيق
// ==========================================

class SyncService {
    constructor() {
        this.syncQueue = [];
        this.isSyncing = false;
        this.lastSync = null;
    }

    /**
     * إضافة عملية للطابور
     */
    addToQueue(operation) {
        this.syncQueue.push({
            operation,
            timestamp: Date.now(),
            status: 'pending'
        });
    }

    /**
     * مزامنة الطابور
     */
    async sync() {
        if (this.isSyncing) return;
        
        this.isSyncing = true;
        
        while (this.syncQueue.length > 0) {
            const item = this.syncQueue[0];
            
            try {
                // محاكاة التأخير
                await new Promise(resolve => setTimeout(resolve, 100));
                item.status = 'completed';
                this.syncQueue.shift();
            } catch (error) {
                item.status = 'failed';
                console.error('❌ خطأ في المزامنة:', error);
                break;
            }
        }
        
        this.lastSync = Date.now();
        this.isSyncing = false;
    }

    /**
     * الحصول على حالة المزامنة
     */
    getStatus() {
        return {
            isSyncing: this.isSyncing,
            queueLength: this.syncQueue.length,
            lastSync: this.lastSync,
            queue: this.syncQueue
        };
    }
}

// ==========================================
// 5️⃣ خدمة الإشعارات
// ==========================================

class NotificationService {
    static show(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            background: ${this.getColor(type)};
            color: white;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        if (duration > 0) {
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, duration);
        }
        
        return notification;
    }

    static getColor(type) {
        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        };
        return colors[type] || colors.info;
    }

    static success(message, duration = 3000) {
        return this.show(message, 'success', duration);
    }

    static error(message, duration = 3000) {
        return this.show(message, 'error', duration);
    }

    static warning(message, duration = 3000) {
        return this.show(message, 'warning', duration);
    }

    static info(message, duration = 3000) {
        return this.show(message, 'info', duration);
    }
}

// ==========================================
// 6️⃣ خدمة المساعدة والتوثيق
// ==========================================

class HelpService {
    static tips = {
        calculator: 'اختر عدد الجدران + مكان التصويب + قياس البيضا = النظام يحسب قياس العصا',
        dashboard: 'شاهد جميع إحصائياتك والمقاييس المحفوظة',
        editor: 'عدّل أو احذف المقاييس الموجودة',
        export: 'صدّر بياناتك كـ JSON أو CSV للحفاظ عليها'
    };

    static tutorials = {
        'getting-started': 'ابدأ باختيار الوضع المطلوب من القائمة العلوية',
        'adding-measurements': 'استخدم واجهة الحساب لإضافة قياسات جديدة',
        'exporting-data': 'اذهب إلى الإعدادات واختر تصدير البيانات',
        'importing-data': 'استعد بياناتك السابقة من ملف محفوظ'
    };

    static getTip(section) {
        return this.tips[section] || 'لا توجد نصيحة متاحة';
    }

    static getTutorial(topic) {
        return this.tutorials[topic] || 'لا يوجد درس متاح';
    }

    static getAll() {
        return {
            tips: this.tips,
            tutorials: this.tutorials
        };
    }
}

// ==========================================
// تصدير الخدمات
// ==========================================

// إنشاء نسخ عامة من الخدمات
const storageService = new StorageService();
const analyticsService = new AnalyticsService();
const syncService = new SyncService();

// تصدير للاستخدام العام
window.Services = {
    Storage: storageService,
    Export: ExportService,
    Analytics: analyticsService,
    Sync: syncService,
    Notification: NotificationService,
    Help: HelpService
};

console.log('✅ خدمات النظام المركزية جاهزة');
