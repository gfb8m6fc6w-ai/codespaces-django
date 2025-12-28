/**
 * ⚡ خدمة تحسين الأداء والـ Caching
 * 
 * توفر caching وتحسينات أداء شاملة للتطبيق
 */

// ==========================================
// 1️⃣ نظام الـ Cache
// ==========================================

class CacheService {
    constructor(ttl = 60000) { // 1 دقيقة افتراضياً
        this.cache = new Map();
        this.ttl = ttl;
        this.stats = {
            hits: 0,
            misses: 0,
            sets: 0
        };
    }

    /**
     * إعداد قيمة في الـ cache
     */
    set(key, value, ttl = this.ttl) {
        const expires = Date.now() + ttl;
        this.cache.set(key, { value, expires });
        this.stats.sets++;
        return value;
    }

    /**
     * الحصول على قيمة من الـ cache
     */
    get(key) {
        const item = this.cache.get(key);

        if (!item) {
            this.stats.misses++;
            return null;
        }

        // التحقق من انتهاء الصلاحية
        if (Date.now() > item.expires) {
            this.cache.delete(key);
            this.stats.misses++;
            return null;
        }

        this.stats.hits++;
        return item.value;
    }

    /**
     * حذف عنصر
     */
    delete(key) {
        return this.cache.delete(key);
    }

    /**
     * مسح كل الـ cache
     */
    clear() {
        this.cache.clear();
        return { success: true, cleared: true };
    }

    /**
     * حذف العناصر المنتهية الصلاحية
     */
    cleanup() {
        const now = Date.now();
        let cleaned = 0;

        for (let [key, { expires }] of this.cache) {
            if (now > expires) {
                this.cache.delete(key);
                cleaned++;
            }
        }

        return { cleaned, remaining: this.cache.size };
    }

    /**
     * الحصول على الإحصائيات
     */
    getStats() {
        const total = this.stats.hits + this.stats.misses;
        return {
            ...this.stats,
            total,
            hitRate: total === 0 ? '0%' : `${((this.stats.hits / total) * 100).toFixed(2)}%`,
            size: this.cache.size
        };
    }

    /**
     * تعيين حد أقصى لحجم الـ cache
     */
    setMaxSize(maxSize) {
        this.maxSize = maxSize;
        this.enforceMaxSize();
    }

    /**
     * فرض حد أقصى لحجم الـ cache
     */
    enforceMaxSize() {
        if (this.maxSize && this.cache.size > this.maxSize) {
            const toDelete = this.cache.size - this.maxSize;
            const keys = Array.from(this.cache.keys());
            for (let i = 0; i < toDelete; i++) {
                this.cache.delete(keys[i]);
            }
        }
    }
}

// ==========================================
// 2️⃣ نظام Pagination
// ==========================================

class PaginationService {
    constructor(items = [], pageSize = 10) {
        this.items = items;
        this.pageSize = pageSize;
        this.currentPage = 1;
        this.updatePageInfo();
    }

    /**
     * تحديث معلومات الصفحات
     */
    updatePageInfo() {
        this.totalPages = Math.ceil(this.items.length / this.pageSize);
        if (this.currentPage > this.totalPages) {
            this.currentPage = Math.max(1, this.totalPages);
        }
    }

    /**
     * الحصول على صفحة محددة
     */
    getPage(pageNumber = this.currentPage) {
        const start = (pageNumber - 1) * this.pageSize;
        const end = start + this.pageSize;
        return this.items.slice(start, end);
    }

    /**
     * الصفحة التالية
     */
    nextPage() {
        if (this.currentPage < this.totalPages) {
            this.currentPage++;
        }
        return this.getPage(this.currentPage);
    }

    /**
     * الصفحة السابقة
     */
    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
        }
        return this.getPage(this.currentPage);
    }

    /**
     * الذهاب إلى صفحة محددة
     */
    goToPage(pageNumber) {
        if (pageNumber >= 1 && pageNumber <= this.totalPages) {
            this.currentPage = pageNumber;
            return this.getPage(this.currentPage);
        }
        return null;
    }

    /**
     * الصفحة الأولى
     */
    firstPage() {
        this.currentPage = 1;
        return this.getPage(1);
    }

    /**
     * الصفحة الأخيرة
     */
    lastPage() {
        this.currentPage = this.totalPages;
        return this.getPage(this.totalPages);
    }

    /**
     * معلومات الصفحات
     */
    getInfo() {
        return {
            currentPage: this.currentPage,
            totalPages: this.totalPages,
            pageSize: this.pageSize,
            totalItems: this.items.length,
            startIndex: (this.currentPage - 1) * this.pageSize + 1,
            endIndex: Math.min(this.currentPage * this.pageSize, this.items.length)
        };
    }

    /**
     * تحديث البيانات
     */
    setItems(items) {
        this.items = items;
        this.updatePageInfo();
        return this.getPage(1);
    }

    /**
     * تحديث حجم الصفحة
     */
    setPageSize(pageSize) {
        this.pageSize = pageSize;
        this.updatePageInfo();
        return this.getPage(this.currentPage);
    }

    /**
     * البحث والتصفيف مع الـ pagination
     */
    search(searchFn) {
        this.items = this.items.filter(searchFn);
        this.updatePageInfo();
        return this.getPage(1);
    }

    /**
     * الترتيب مع الـ pagination
     */
    sort(compareFn) {
        this.items.sort(compareFn);
        return this.getPage(this.currentPage);
    }
}

// ==========================================
// 3️⃣ نظام البحث والفلترة
// ==========================================

class SearchFilterService {
    constructor(items = []) {
        this.items = items;
        this.filters = {};
        this.searchQuery = '';
    }

    /**
     * البحث في البيانات
     */
    search(query, fields = null) {
        this.searchQuery = query.toLowerCase();

        if (!this.searchQuery) {
            return this.applyFilters();
        }

        let results = this.items;

        if (fields) {
            // البحث في حقول محددة
            results = results.filter(item =>
                fields.some(field =>
                    String(item[field]).toLowerCase().includes(this.searchQuery)
                )
            );
        } else {
            // البحث في جميع الحقول
            results = results.filter(item =>
                JSON.stringify(item).toLowerCase().includes(this.searchQuery)
            );
        }

        return this.applyFilters(results);
    }

    /**
     * إضافة فلتر
     */
    addFilter(key, value) {
        if (!this.filters[key]) {
            this.filters[key] = [];
        }

        if (Array.isArray(value)) {
            this.filters[key].push(...value);
        } else {
            if (!this.filters[key].includes(value)) {
                this.filters[key].push(value);
            }
        }

        return this.applyFilters();
    }

    /**
     * إزالة فلتر
     */
    removeFilter(key, value) {
        if (this.filters[key]) {
            this.filters[key] = this.filters[key].filter(v => v !== value);
            if (this.filters[key].length === 0) {
                delete this.filters[key];
            }
        }
        return this.applyFilters();
    }

    /**
     * تطبيق الفلاتر
     */
    applyFilters(items = this.items) {
        let results = items;

        Object.entries(this.filters).forEach(([key, values]) => {
            results = results.filter(item => values.includes(item[key]));
        });

        return results;
    }

    /**
     * مسح جميع الفلاتر
     */
    clearFilters() {
        this.filters = {};
        this.searchQuery = '';
        return this.items;
    }

    /**
     * الحصول على الفلاتر الفعالة
     */
    getActiveFilters() {
        return {
            search: this.searchQuery,
            filters: this.filters,
            activeFilterCount: Object.keys(this.filters).length
        };
    }

    /**
     * إحصائيات البحث والفلاتر
     */
    getStats(results) {
        const total = this.items.length;
        const filtered = results.length;
        return {
            total,
            filtered,
            removed: total - filtered,
            percentage: `${((filtered / total) * 100).toFixed(2)}%`
        };
    }
}

// ==========================================
// 4️⃣ أداة تحسين الأداء
// ==========================================

class PerformanceOptimizer {
    constructor() {
        this.timings = {};
        this.operations = [];
    }

    /**
     * قياس سرعة عملية
     */
    measure(name, fn) {
        const start = performance.now();
        let result = null;
        let error = null;

        try {
            result = fn();
        } catch (e) {
            error = e;
        }

        const duration = performance.now() - start;

        const timing = {
            name,
            duration: duration.toFixed(2),
            timestamp: new Date().toISOString(),
            error: error ? error.message : null
        };

        this.timings[name] = timing;
        this.operations.push(timing);

        if (error) throw error;
        return result;
    }

    /**
     * قياس عملية متزامنة
     */
    async measureAsync(name, fn) {
        const start = performance.now();
        let result = null;
        let error = null;

        try {
            result = await fn();
        } catch (e) {
            error = e;
        }

        const duration = performance.now() - start;

        const timing = {
            name,
            duration: duration.toFixed(2),
            timestamp: new Date().toISOString(),
            async: true,
            error: error ? error.message : null
        };

        this.timings[name] = timing;
        this.operations.push(timing);

        if (error) throw error;
        return result;
    }

    /**
     * الحصول على الأوقات
     */
    getTimings() {
        return this.timings;
    }

    /**
     * الحصول على أبطأ العمليات
     */
    getSlowest(count = 5) {
        return this.operations
            .sort((a, b) => parseFloat(b.duration) - parseFloat(a.duration))
            .slice(0, count);
    }

    /**
     * الحصول على أسرع العمليات
     */
    getFastest(count = 5) {
        return this.operations
            .sort((a, b) => parseFloat(a.duration) - parseFloat(b.duration))
            .slice(0, count);
    }

    /**
     * متوسط سرعة العمليات
     */
    getAverageTime(name) {
        const operations = this.operations.filter(op => op.name === name);
        if (operations.length === 0) return 0;

        const total = operations.reduce((sum, op) => sum + parseFloat(op.duration), 0);
        return (total / operations.length).toFixed(2);
    }

    /**
     * تقرير الأداء
     */
    getReport() {
        return {
            totalOperations: this.operations.length,
            totalTime: this.operations.reduce((sum, op) => sum + parseFloat(op.duration), 0).toFixed(2),
            averageTime: (this.operations.reduce((sum, op) => sum + parseFloat(op.duration), 0) / this.operations.length).toFixed(2),
            slowest: this.getSlowest(5),
            fastest: this.getFastest(5)
        };
    }

    /**
     * مسح التوقيتات
     */
    clear() {
        this.timings = {};
        this.operations = [];
    }
}

// ==========================================
// 5️⃣ الاستخدام
// ==========================================

// إنشاء الخدمات
const Cache = new CacheService();
const Pagination = new PaginationService();
const SearchFilter = new SearchFilterService();
const Perf = new PerformanceOptimizer();

// أمثلة على الاستخدام
/*

// استخدام الـ Cache
Cache.set('stats', { total: 100 }, 60000);
const stats = Cache.get('stats');
console.log('⚡ الإحصائيات من الـ cache:', stats);

// استخدام Pagination
const measurements = [/* array of items */];
const paginator = new PaginationService(measurements, 20);
const page1 = paginator.getPage(1);
const nextPage = paginator.nextPage();

// استخدام البحث والفلترة
const searcher = new SearchFilterService(measurements);
const results = searcher.search('billiards');
searcher.addFilter('rails', 2);
const filtered = searcher.applyFilters();

// قياس الأداء
Perf.measure('calculation', () => {
    return engine.calculateCue(3, 2);
});

console.log('📊 تقرير الأداء:', Perf.getReport());

*/
