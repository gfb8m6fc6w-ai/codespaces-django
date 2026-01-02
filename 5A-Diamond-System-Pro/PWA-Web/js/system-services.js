/**
 * 🔧 خدمات نظام البلياردو الموحدة
 * مجموعة شاملة من الخدمات المشتركة
 */

// ==================== مفتاح التخزين الموحد ====================
const STORAGE_KEY = '5a-diamond-system-data';

// ==================== مدير التخزين ====================
class StorageManager {
    constructor(namespace = 'default') {
        this.namespace = namespace;
        this.key = `${STORAGE_KEY}-${namespace}`;
    }

    save(data) {
        try {
            localStorage.setItem(this.key, JSON.stringify(data));
            return true;
        } catch (e) {
            console.error('❌ خطأ في حفظ البيانات:', e);
            return false;
        }
    }

    load() {
        try {
            const data = localStorage.getItem(this.key);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.error('❌ خطأ في تحميل البيانات:', e);
            return null;
        }
    }

    delete() {
        try {
            localStorage.removeItem(this.key);
            return true;
        } catch (e) {
            console.error('❌ خطأ في حذف البيانات:', e);
            return false;
        }
    }

    clear() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith(STORAGE_KEY)) {
                    localStorage.removeItem(key);
                }
            });
            return true;
        } catch (e) {
            console.error('❌ خطأ في مسح البيانات:', e);
            return false;
        }
    }
}

// ==================== مدير الإشعارات ====================
class NotificationManager {
    static show(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            background: ${this._getColor(type)};
            color: white;
            border-radius: 6px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }

    static _getColor(type) {
        const colors = {
            success: '#16c784',
            error: '#e94560',
            warning: '#f39c12',
            info: '#0066cc'
        };
        return colors[type] || colors.info;
    }
}

// ==================== مدير التصدير والاستيراد ====================
class ExportImportManager {
    static export(data, filename = 'billiards-data.json') {
        const dataStr = JSON.stringify(data, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    static import(file, onSuccess, onError) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);
                onSuccess(data);
                NotificationManager.show('✅ تم استيراد البيانات بنجاح', 'success');
            } catch (error) {
                onError(error);
                NotificationManager.show('❌ خطأ في استيراد البيانات', 'error');
            }
        };
        reader.readAsText(file);
    }
}

// ==================== مدير النسخ الاحتياطية ====================
class BackupManager {
    constructor(namespace = 'backups') {
        this.storage = new StorageManager(namespace);
    }

    createBackup(data) {
        const backups = this.storage.load() || [];
        const backup = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            data: data
        };
        backups.push(backup);
        // احتفظ فقط بآخر 10 نسخ احتياطية
        if (backups.length > 10) {
            backups.shift();
        }
        this.storage.save(backups);
        return backup;
    }

    restoreBackup(backupId) {
        const backups = this.storage.load() || [];
        const backup = backups.find(b => b.id === backupId);
        if (backup) {
            return backup.data;
        }
        return null;
    }

    listBackups() {
        return (this.storage.load() || []).map(b => ({
            id: b.id,
            timestamp: b.timestamp
        }));
    }

    deleteBackup(backupId) {
        const backups = this.storage.load() || [];
        const filtered = backups.filter(b => b.id !== backupId);
        this.storage.save(filtered);
    }
}

// ==================== مدير التحديثات ====================
class UpdateManager {
    static checkForUpdates() {
        return fetch('./manifest.json')
            .then(response => response.json())
            .then(data => {
                const currentVersion = localStorage.getItem(STORAGE_KEY + '-version');
                if (currentVersion !== data.version) {
                    localStorage.setItem(STORAGE_KEY + '-version', data.version);
                    NotificationManager.show('✅ تحديث جديد متاح', 'success');
                    return true;
                }
                return false;
            })
            .catch(error => {
                console.error('❌ خطأ في التحقق من التحديثات:', error);
                return false;
            });
    }
}

// ==================== مدير الوضع الليلي ====================
class ThemeManager {
    constructor() {
        this.themes = {
            dark: {
                bg: '#1a1a2e',
                text: '#eee',
                primary: '#16c784',
                secondary: '#0f3460',
                danger: '#e94560',
                accent: '#f39c12'
            },
            light: {
                bg: '#f8f9fa',
                text: '#212529',
                primary: '#667eea',
                secondary: '#764ba2',
                danger: '#e74c3c',
                accent: '#ffc107'
            }
        };
        this.storage = new StorageManager('theme');
        this.currentTheme = this.storage.load() || 'dark';
    }

    setTheme(themeName) {
        if (this.themes[themeName]) {
            this.currentTheme = themeName;
            this.storage.save(themeName);
            this.applyTheme();
            NotificationManager.show(`تم تبديل الوضع إلى ${themeName === 'dark' ? 'ليلي' : 'نهاري'}`, 'info');
        }
    }

    getTheme() {
        return this.themes[this.currentTheme];
    }

    applyTheme() {
        const theme = this.getTheme();
        document.documentElement.style.cssText = `
            --bg-color: ${theme.bg};
            --text-color: ${theme.text};
            --primary-color: ${theme.primary};
            --secondary-color: ${theme.secondary};
            --danger-color: ${theme.danger};
            --accent-color: ${theme.accent};
        `;
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
}

// ==================== مدير الأداء ====================
class PerformanceManager {
    static measureFunction(functionName, fn) {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        const duration = end - start;
        console.log(`⏱️ ${functionName}: ${duration.toFixed(2)}ms`);
        return result;
    }

    static logMetrics() {
        const metrics = {
            memory: performance.memory,
            navigation: performance.getEntriesByType('navigation')[0]
        };
        console.table(metrics);
    }
}

// ==================== تحديثات CSS ====================
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    :root {
        --bg-color: #1a1a2e;
        --text-color: #eee;
        --primary-color: #16c784;
        --secondary-color: #0f3460;
        --danger-color: #e94560;
        --accent-color: #f39c12;
    }
`;
document.head.appendChild(styleSheet);

// ==================== تصدير الخدمات ====================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        STORAGE_KEY,
        StorageManager,
        NotificationManager,
        ExportImportManager,
        BackupManager,
        UpdateManager,
        ThemeManager,
        PerformanceManager
    };
}

console.log('✅ تم تحميل خدمات النظام الموحدة');
