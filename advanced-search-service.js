/**
 * 🔍 خدمة البحث والفلترة المتقدمة
 * 
 * توفر بحث وفلترة متقدمة مع دعم الفلاتر المتعددة
 */

class AdvancedSearchFilter {
    constructor(items = []) {
        this.items = items;
        this.filters = {};
        this.searchQuery = '';
        this.sortConfig = { field: null, ascending: true };
        this.history = [];
        this.maxHistorySize = 20;
    }

    /**
     * البحث المتقدم
     */
    search(query, options = {}) {
        const {
            fields = null,
            caseSensitive = false,
            exact = false,
            regex = false
        } = options;

        if (!query) {
            this.searchQuery = '';
            return this.getResults();
        }

        this.searchQuery = caseSensitive ? query : query.toLowerCase();
        this.addToHistory('search', { query, options });

        let results = this.items;

        if (regex) {
            try {
                const pattern = new RegExp(this.searchQuery, caseSensitive ? 'g' : 'gi');
                results = results.filter(item =>
                    fields
                        ? fields.some(f => pattern.test(String(item[f])))
                        : pattern.test(JSON.stringify(item))
                );
            } catch (e) {
                console.warn('⚠️ خطأ في regex:', e.message);
                return [];
            }
        } else if (exact) {
            results = results.filter(item =>
                fields
                    ? fields.some(f => {
                        const value = String(item[f]);
                        return caseSensitive
                            ? value === this.searchQuery
                            : value.toLowerCase() === this.searchQuery;
                    })
                    : JSON.stringify(item).toLowerCase() === this.searchQuery
            );
        } else {
            results = results.filter(item =>
                fields
                    ? fields.some(f => {
                        const value = String(item[f]);
                        return caseSensitive
                            ? value.includes(this.searchQuery)
                            : value.toLowerCase().includes(this.searchQuery);
                    })
                    : JSON.stringify(item).toLowerCase().includes(this.searchQuery)
            );
        }

        return this.applyFilters(results);
    }

    /**
     * فلترة متقدمة
     */
    addAdvancedFilter(key, operator, value) {
        if (!this.filters[key]) {
            this.filters[key] = [];
        }

        this.filters[key].push({ operator, value });
        this.addToHistory('filter', { key, operator, value });

        return this.getResults();
    }

    /**
     * العمليات المدعومة:
     * equals (=), not equals (!=)
     * greater (>), less (<)
     * greater or equal (>=), less or equal (<=)
     * contains, not contains
     * in, not in
     * between
     */
    evaluateFilter(itemValue, operator, filterValue) {
        switch (operator) {
            case '=':
            case 'equals':
                return itemValue === filterValue;
            case '!=':
            case 'not equals':
                return itemValue !== filterValue;
            case '>':
            case 'greater':
                return itemValue > filterValue;
            case '<':
            case 'less':
                return itemValue < filterValue;
            case '>=':
            case 'greater or equal':
                return itemValue >= filterValue;
            case '<=':
            case 'less or equal':
                return itemValue <= filterValue;
            case 'contains':
                return String(itemValue).toLowerCase().includes(String(filterValue).toLowerCase());
            case 'not contains':
                return !String(itemValue).toLowerCase().includes(String(filterValue).toLowerCase());
            case 'in':
                return Array.isArray(filterValue) ? filterValue.includes(itemValue) : false;
            case 'not in':
                return Array.isArray(filterValue) ? !filterValue.includes(itemValue) : true;
            case 'between':
                return Array.isArray(filterValue) && filterValue.length === 2
                    ? itemValue >= filterValue[0] && itemValue <= filterValue[1]
                    : false;
            case 'exists':
                return itemValue !== null && itemValue !== undefined;
            case 'not exists':
                return itemValue === null || itemValue === undefined;
            default:
                return true;
        }
    }

    /**
     * تطبيق جميع الفلاتر
     */
    applyFilters(items = this.items) {
        let results = items;

        Object.entries(this.filters).forEach(([key, filterArray]) => {
            results = results.filter(item => {
                return filterArray.every(filter =>
                    this.evaluateFilter(item[key], filter.operator, filter.value)
                );
            });
        });

        return results;
    }

    /**
     * الترتيب
     */
    sort(field, ascending = true) {
        this.sortConfig = { field, ascending };
        this.addToHistory('sort', { field, ascending });

        return this.getResults();
    }

    /**
     * تطبيق الترتيب
     */
    applySorting(items) {
        if (!this.sortConfig.field) {
            return items;
        }

        const sorted = [...items];
        sorted.sort((a, b) => {
            const aVal = a[this.sortConfig.field];
            const bVal = b[this.sortConfig.field];

            let comparison = 0;
            if (aVal > bVal) comparison = 1;
            else if (aVal < bVal) comparison = -1;

            return this.sortConfig.ascending ? comparison : -comparison;
        });

        return sorted;
    }

    /**
     * الحصول على النتائج النهائية
     */
    getResults() {
        let results = this.applyFilters();
        results = this.applySorting(results);
        return results;
    }

    /**
     * تجميع النتائج
     */
    groupBy(field) {
        const results = this.getResults();
        const grouped = {};

        results.forEach(item => {
            const key = item[field];
            if (!grouped[key]) {
                grouped[key] = [];
            }
            grouped[key].push(item);
        });

        return grouped;
    }

    /**
     * تجميع وعد العناصر
     */
    countBy(field) {
        const results = this.getResults();
        const counts = {};

        results.forEach(item => {
            const key = item[field];
            counts[key] = (counts[key] || 0) + 1;
        });

        return counts;
    }

    /**
     * الحصول على الإحصائيات
     */
    getStatistics() {
        const results = this.getResults();
        const total = this.items.length;

        return {
            total,
            filtered: results.length,
            removed: total - results.length,
            percentage: ((results.length / total) * 100).toFixed(2) + '%',
            activeFilters: Object.keys(this.filters).length,
            hasSearch: !!this.searchQuery,
            hasSort: !!this.sortConfig.field
        };
    }

    /**
     * مسح كل شيء
     */
    clearAll() {
        this.filters = {};
        this.searchQuery = '';
        this.sortConfig = { field: null, ascending: true };
        return this.items;
    }

    /**
     * مسح البحث
     */
    clearSearch() {
        this.searchQuery = '';
        return this.getResults();
    }

    /**
     * مسح الفلاتر
     */
    clearFilters() {
        this.filters = {};
        return this.getResults();
    }

    /**
     * مسح الترتيب
     */
    clearSort() {
        this.sortConfig = { field: null, ascending: true };
        return this.getResults();
    }

    /**
     * إضافة إلى السجل
     */
    addToHistory(action, data) {
        this.history.push({
            action,
            data,
            timestamp: new Date().toISOString()
        });

        // احتفظ بآخر 20 عملية فقط
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
        }
    }

    /**
     * الحصول على السجل
     */
    getHistory() {
        return this.history;
    }

    /**
     * الرجوع للخطوة السابقة
     */
    undo() {
        if (this.history.length === 0) {
            return this.getResults();
        }

        this.history.pop();

        // إعادة بناء الحالة من السجل
        this.filters = {};
        this.searchQuery = '';
        this.sortConfig = { field: null, ascending: true };

        this.history.forEach(({ action, data }) => {
            if (action === 'search') {
                this.search(data.query, data.options);
            } else if (action === 'filter') {
                this.addAdvancedFilter(data.key, data.operator, data.value);
            } else if (action === 'sort') {
                this.sort(data.field, data.ascending);
            }
        });

        return this.getResults();
    }

    /**
     * تصدير الفلاتر الحالية
     */
    exportFilters() {
        return {
            search: this.searchQuery,
            filters: this.filters,
            sort: this.sortConfig,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * استيراد الفلاتر
     */
    importFilters(config) {
        if (config.search) this.searchQuery = config.search;
        if (config.filters) this.filters = config.filters;
        if (config.sort) this.sortConfig = config.sort;
        return this.getResults();
    }

    /**
     * إنشاء حفظة (Snapshot)
     */
    createSnapshot() {
        return {
            items: JSON.parse(JSON.stringify(this.items)),
            config: this.exportFilters(),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * استعادة من حفظة
     */
    restoreSnapshot(snapshot) {
        this.items = JSON.parse(JSON.stringify(snapshot.items));
        this.importFilters(snapshot.config);
        return this.getResults();
    }
}

// ==========================================
// الاستخدام
// ==========================================

/*

const searcher = new AdvancedSearchFilter(measurements);

// بحث بسيط
const results1 = searcher.search('billiards');

// بحث في حقول محددة
const results2 = searcher.search('3', { fields: ['rails', 'target'] });

// فلاتر متقدمة
searcher.addAdvancedFilter('rails', '=', 2);
searcher.addAdvancedFilter('target', '>', 3);
searcher.addAdvancedFilter('target', '<', 5);

// الترتيب
searcher.sort('date', false); // بترتيب تنازلي

// الحصول على النتائج
const filtered = searcher.getResults();

// التجميع
const groupedByRails = searcher.groupBy('rails');

// الإحصائيات
console.log(searcher.getStatistics());

// الرجوع للخطوة السابقة
searcher.undo();

*/
