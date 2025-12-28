/**
 * 🛡️ خدمة معالجة الأخطاء والتحقق من البيانات
 * 
 * توفر معالجة شاملة للأخطاء والتحقق من صحة البيانات
 */

// ==========================================
// 1️⃣ نظام الأخطاء المخصصة
// ==========================================

class BilliardsError extends Error {
    constructor(message, code, details = {}) {
        super(message);
        this.name = 'BilliardsError';
        this.code = code;
        this.details = details;
        this.timestamp = new Date().toISOString();
    }

    toString() {
        return `[${this.code}] ${this.message} (${this.timestamp})`;
    }

    toJSON() {
        return {
            name: this.name,
            message: this.message,
            code: this.code,
            details: this.details,
            timestamp: this.timestamp
        };
    }
}

// أنواع الأخطاء المختلفة
class ValidationError extends BilliardsError {
    constructor(message, details) {
        super(message, 'VALIDATION_ERROR', details);
    }
}

class StorageError extends BilliardsError {
    constructor(message, details) {
        super(message, 'STORAGE_ERROR', details);
    }
}

class CalculationError extends BilliardsError {
    constructor(message, details) {
        super(message, 'CALCULATION_ERROR', details);
    }
}

// ==========================================
// 2️⃣ نظام التحقق من البيانات
// ==========================================

class DataValidator {
    /**
     * التحقق من قياس واحد
     */
    static validateMeasurement(data) {
        const errors = [];
        const warnings = [];

        // التحقق من وجود البيانات
        if (!data) {
            errors.push('البيانات فارغة');
            return { valid: false, errors, warnings };
        }

        // التحقق من الجدران
        if (data.rails === undefined || data.rails === null) {
            errors.push('عدد الجدران مطلوب');
        } else if (!Number.isInteger(data.rails) || data.rails < 1 || data.rails > 4) {
            errors.push('الجدران يجب أن تكون من 1 إلى 4');
        }

        // التحقق من الأرقام العشرية
        const numericFields = {
            target: { min: 0, max: 10, name: 'التصويب' },
            whiteBall: { min: 0, max: 10, name: 'البيضا' },
            expectedCue: { min: 0, max: 20, name: 'العصا المتوقع' }
        };

        Object.entries(numericFields).forEach(([field, config]) => {
            if (data[field] === undefined || data[field] === null) {
                errors.push(`${config.name} مطلوب`);
            } else {
                const value = parseFloat(data[field]);
                if (isNaN(value)) {
                    errors.push(`${config.name} يجب أن يكون رقماً`);
                } else if (value < config.min || value > config.max) {
                    errors.push(`${config.name} يجب أن يكون بين ${config.min} و ${config.max}`);
                }
            }
        });

        // التحقق من الحساب (إن وجد)
        if (data.target !== undefined && data.whiteBall !== undefined && data.expectedCue !== undefined) {
            const target = parseFloat(data.target);
            const whiteBall = parseFloat(data.whiteBall);
            const expectedCue = parseFloat(data.expectedCue);

            if (!isNaN(target) && !isNaN(whiteBall) && !isNaN(expectedCue)) {
                const calculated = parseFloat((target + whiteBall).toFixed(1));
                const diff = Math.abs(calculated - expectedCue);

                if (diff > 0.15) {
                    warnings.push(`⚠️ الحساب قد يكون خاطئاً (الفرق: ${diff.toFixed(2)})`);
                }
            }
        }

        // التحقق من التاريخ (اختياري)
        if (data.date && isNaN(Date.parse(data.date))) {
            errors.push('التاريخ غير صحيح');
        }

        return {
            valid: errors.length === 0,
            errors,
            warnings
        };
    }

    /**
     * التحقق من مجموعة من القياسات
     */
    static validateBulk(measurements) {
        if (!Array.isArray(measurements)) {
            return {
                valid: false,
                errors: ['البيانات يجب أن تكون مصفوفة'],
                totalChecked: 0,
                validCount: 0,
                invalidCount: 0
            };
        }

        let validCount = 0;
        const allErrors = [];

        measurements.forEach((m, index) => {
            const validation = this.validateMeasurement(m);
            if (validation.valid) {
                validCount++;
            } else {
                allErrors.push({
                    index,
                    errors: validation.errors
                });
            }
        });

        return {
            valid: allErrors.length === 0,
            errors: allErrors,
            totalChecked: measurements.length,
            validCount,
            invalidCount: measurements.length - validCount,
            successRate: `${((validCount / measurements.length) * 100).toFixed(2)}%`
        };
    }

    /**
     * تطهير البيانات
     */
    static sanitizeData(data) {
        const sanitized = { ...data };

        // تحويل الأرقام
        if (sanitized.target) sanitized.target = parseFloat(sanitized.target);
        if (sanitized.whiteBall) sanitized.whiteBall = parseFloat(sanitized.whiteBall);
        if (sanitized.expectedCue) sanitized.expectedCue = parseFloat(sanitized.expectedCue);
        if (sanitized.rails) sanitized.rails = parseInt(sanitized.rails);

        // تنظيف النصوص
        if (sanitized.notes) {
            sanitized.notes = String(sanitized.notes).trim();
        }

        return sanitized;
    }
}

// ==========================================
// 3️⃣ نظام معالجة الأخطاء
// ==========================================

class ErrorHandler {
    constructor() {
        this.errorLog = [];
        this.errorListeners = [];
        this.setupGlobalHandlers();
    }

    /**
     * إعداد معالجات الأخطاء العامة
     */
    setupGlobalHandlers() {
        window.addEventListener('error', (event) => {
            this.handleError(
                new BilliardsError(
                    event.message,
                    'UNCAUGHT_ERROR',
                    { filename: event.filename, lineno: event.lineno }
                )
            );
        });

        window.addEventListener('unhandledrejection', (event) => {
            this.handleError(
                new BilliardsError(
                    event.reason || 'Promise rejection',
                    'UNHANDLED_REJECTION'
                )
            );
        });
    }

    /**
     * معالجة خطأ
     */
    handleError(error, context = {}) {
        // تسجيل الخطأ
        const errorEntry = {
            error: error instanceof BilliardsError ? error.toJSON() : { message: String(error) },
            context,
            timestamp: new Date().toISOString(),
            stack: error.stack
        };

        this.errorLog.push(errorEntry);

        // إبلاغ المستمعين
        this.notifyListeners(errorEntry);

        // طباعة في console
        console.error(`❌ ${error.toString()}`);

        return errorEntry;
    }

    /**
     * إضافة مستمع للأخطاء
     */
    onError(callback) {
        this.errorListeners.push(callback);
    }

    /**
     * إبلاغ المستمعين
     */
    notifyListeners(errorEntry) {
        this.errorListeners.forEach(listener => {
            try {
                listener(errorEntry);
            } catch (e) {
                console.error('خطأ في معالج الأخطاء:', e);
            }
        });
    }

    /**
     * الحصول على سجل الأخطاء
     */
    getLog(limit = 50) {
        return this.errorLog.slice(-limit);
    }

    /**
     * مسح السجل
     */
    clearLog() {
        this.errorLog = [];
    }

    /**
     * تصدير سجل الأخطاء
     */
    exportLog() {
        return {
            timestamp: new Date().toISOString(),
            totalErrors: this.errorLog.length,
            errors: this.errorLog
        };
    }
}

// ==========================================
// 4️⃣ نظام السلامة (Fallback)
// ==========================================

class SafetyNet {
    /**
     * تنفيذ آمن للدالة
     */
    static safeExecute(fn, fallback = null, errorHandler = null) {
        try {
            return fn();
        } catch (error) {
            if (errorHandler) {
                errorHandler(error);
            }
            return fallback;
        }
    }

    /**
     * تنفيذ متزامن آمن
     */
    static async safeAsync(promise, fallback = null, timeout = 10000) {
        try {
            return await Promise.race([
                promise,
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error('Timeout')), timeout)
                )
            ]);
        } catch (error) {
            console.warn('⚠️ خطأ في العملية المتزامنة:', error.message);
            return fallback;
        }
    }

    /**
     * التحقق من صحة التخزين المحلي
     */
    static checkLocalStorage() {
        try {
            const test = '__storage_test__';
            localStorage.setItem(test, test);
            localStorage.removeItem(test);
            return { available: true };
        } catch (error) {
            return {
                available: false,
                reason: error.message,
                suggestion: 'قد يكون التخزين ممتلئاً أو معطلاً'
            };
        }
    }

    /**
     * حساب حجم البيانات
     */
    static getStorageSize(data) {
        return new Blob([JSON.stringify(data)]).size;
    }

    /**
     * التحقق من كفاية المساحة
     */
    static checkStorageSpace(dataSize, limit = 5 * 1024 * 1024) {
        const available = limit;
        const percentage = (dataSize / available) * 100;

        return {
            dataSize,
            available,
            percentage: percentage.toFixed(2),
            sufficient: dataSize < available,
            warning: percentage > 80
        };
    }
}

// ==========================================
// 5️⃣ أداة تشخيص النظام
// ==========================================

class SystemDiagnostics {
    static diagnose() {
        return {
            timestamp: new Date().toISOString(),
            environment: {
                userAgent: navigator.userAgent,
                language: navigator.language,
                online: navigator.onLine
            },
            storage: SafetyNet.checkLocalStorage(),
            performance: this.getPerformanceMetrics(),
            memory: this.getMemoryMetrics()
        };
    }

    static getPerformanceMetrics() {
        if (!window.performance) {
            return { supported: false };
        }

        const perf = performance.timing;
        return {
            loadTime: perf.loadEventEnd - perf.navigationStart,
            domReady: perf.domContentLoadedEventEnd - perf.navigationStart,
            firstPaint: perf.responseEnd - perf.navigationStart
        };
    }

    static getMemoryMetrics() {
        if (!performance.memory) {
            return { supported: false };
        }

        return {
            usedJSHeapSize: (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + ' MB',
            jsHeapSizeLimit: (performance.memory.jsHeapSizeLimit / 1048576).toFixed(2) + ' MB',
            usagePercentage: ((performance.memory.usedJSHeapSize / performance.memory.jsHeapSizeLimit) * 100).toFixed(2) + '%'
        };
    }

    static printReport() {
        const report = this.diagnose();
        console.group('📊 تقرير تشخيص النظام');
        console.log(JSON.stringify(report, null, 2));
        console.groupEnd();
        return report;
    }
}

// ==========================================
// 6️⃣ الاستخدام
// ==========================================

// إنشاء معالج الأخطاء
const ErrorHandlerInstance = new SafetyNet();
const ErrorLog = new ErrorHandler();

// أمثلة على الاستخدام
/*

// التحقق من البيانات
const validation = DataValidator.validateMeasurement({
    rails: 2,
    target: 3.5,
    whiteBall: 2.5,
    expectedCue: 6.0
});

if (!validation.valid) {
    console.error('❌ أخطاء:', validation.errors);
}

if (validation.warnings.length > 0) {
    console.warn('⚠️ تحذيرات:', validation.warnings);
}

// معالجة آمنة
const result = SafetyNet.safeExecute(
    () => billiards.calculateCue(3, 2),
    0,
    (error) => ErrorLog.handleError(error)
);

// تشخيص النظام
SystemDiagnostics.printReport();

*/
