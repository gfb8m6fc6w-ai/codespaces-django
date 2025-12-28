/**
 * 🧪 نظام الاختبار الشامل
 * 
 * توفر نظام اختبار بسيط وسهل للاستخدام
 */

class TestRunner {
    constructor() {
        this.suites = [];
        this.results = {
            totalSuites: 0,
            totalTests: 0,
            passed: 0,
            failed: 0,
            skipped: 0,
            time: 0
        };
        this.currentSuite = null;
    }

    /**
     * إنشاء مجموعة اختبارات
     */
    describe(suiteName, fn) {
        this.currentSuite = {
            name: suiteName,
            tests: [],
            status: 'pending'
        };

        fn();
        this.suites.push(this.currentSuite);
        this.currentSuite = null;
    }

    /**
     * إضافة اختبار
     */
    test(testName, fn) {
        if (!this.currentSuite) {
            throw new Error('يجب استدعاء test داخل describe');
        }

        this.currentSuite.tests.push({
            name: testName,
            fn,
            status: 'pending',
            duration: 0,
            error: null
        });
    }

    /**
     * تخطي اختبار
     */
    skip(testName, fn) {
        if (!this.currentSuite) {
            throw new Error('يجب استدعاء skip داخل describe');
        }

        this.currentSuite.tests.push({
            name: testName,
            fn,
            status: 'skipped'
        });
    }

    /**
     * Assertions
     */
    assert(condition, message) {
        if (!condition) {
            throw new Error(`❌ فشل الاختبار: ${message}`);
        }
    }

    equal(actual, expected, message) {
        if (actual !== expected) {
            throw new Error(`❌ ${message || 'القيم غير متساوية'}: ${actual} !== ${expected}`);
        }
    }

    deepEqual(actual, expected, message) {
        const actualStr = JSON.stringify(actual);
        const expectedStr = JSON.stringify(expected);
        if (actualStr !== expectedStr) {
            throw new Error(`❌ ${message || 'القيم غير متساوية'}`);
        }
    }

    throws(fn, message) {
        try {
            fn();
            throw new Error(`❌ ${message || 'كان من المتوقع رمي استثناء'}`);
        } catch (error) {
            if (error.message.startsWith('❌')) throw error;
            // النجاح - تم رمي استثناء
        }
    }

    notThrows(fn, message) {
        try {
            fn();
        } catch (error) {
            throw new Error(`❌ ${message || 'لم يكن من المتوقع رمي استثناء'}: ${error.message}`);
        }
    }

    /**
     * تشغيل جميع الاختبارات
     */
    async run(verbose = true) {
        const startTime = performance.now();

        if (verbose) {
            console.group('🧪 بدء تشغيل الاختبارات');
        }

        for (const suite of this.suites) {
            await this.runSuite(suite, verbose);
        }

        const endTime = performance.now();
        this.results.time = (endTime - startTime).toFixed(2);

        this.printSummary(verbose);

        return this.results;
    }

    /**
     * تشغيل مجموعة اختبارات
     */
    async runSuite(suite, verbose) {
        if (verbose) {
            console.group(`📦 ${suite.name}`);
        }

        this.results.totalSuites++;

        for (const test of suite.tests) {
            await this.runTest(test, verbose);
        }

        if (verbose) {
            console.groupEnd();
        }
    }

    /**
     * تشغيل اختبار واحد
     */
    async runTest(test, verbose) {
        this.results.totalTests++;

        if (test.status === 'skipped') {
            this.results.skipped++;
            if (verbose) {
                console.log(`⏭️ ${test.name}`);
            }
            return;
        }

        const startTime = performance.now();

        try {
            if (test.fn.constructor.name === 'AsyncFunction') {
                await test.fn();
            } else {
                test.fn();
            }

            const duration = performance.now() - startTime;
            test.status = 'passed';
            test.duration = duration.toFixed(2);
            this.results.passed++;

            if (verbose) {
                console.log(`✅ ${test.name} (${test.duration}ms)`);
            }
        } catch (error) {
            const duration = performance.now() - startTime;
            test.status = 'failed';
            test.error = error.message;
            test.duration = duration.toFixed(2);
            this.results.failed++;

            if (verbose) {
                console.error(`❌ ${test.name}\n   ${error.message}`);
            }
        }
    }

    /**
     * طباعة الملخص
     */
    printSummary(verbose = true) {
        const total = this.results.totalTests;
        const passed = this.results.passed;
        const failed = this.results.failed;
        const skipped = this.results.skipped;
        const percentage = total === 0 ? 0 : ((passed / (total - skipped)) * 100).toFixed(2);

        if (verbose) {
            console.log('\n📊 ملخص الاختبارات:');
            console.log(`   ✅ نجح: ${passed}`);
            console.log(`   ❌ فشل: ${failed}`);
            console.log(`   ⏭️ تخطي: ${skipped}`);
            console.log(`   📈 النسبة: ${percentage}%`);
            console.log(`   ⏱️ الوقت الإجمالي: ${this.results.time}ms`);
            console.groupEnd();
        }
    }

    /**
     * الحصول على التقرير المفصل
     */
    getDetailedReport() {
        return {
            summary: this.results,
            suites: this.suites.map(suite => ({
                name: suite.name,
                totalTests: suite.tests.length,
                passed: suite.tests.filter(t => t.status === 'passed').length,
                failed: suite.tests.filter(t => t.status === 'failed').length,
                skipped: suite.tests.filter(t => t.status === 'skipped').length,
                tests: suite.tests.map(test => ({
                    name: test.name,
                    status: test.status,
                    duration: test.duration,
                    error: test.error
                }))
            }))
        };
    }

    /**
     * تصدير النتائج كـ JSON
     */
    exportJSON() {
        return JSON.stringify(this.getDetailedReport(), null, 2);
    }

    /**
     * تصدير النتائج كـ HTML
     */
    exportHTML() {
        const report = this.getDetailedReport();
        let html = `<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <title>تقرير الاختبارات</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .summary { background: #f0f0f0; padding: 15px; margin-bottom: 20px; }
        .suite { background: white; border: 1px solid #ddd; margin-bottom: 15px; }
        .suite-title { background: #667eea; color: white; padding: 10px; }
        .test { padding: 10px; border-bottom: 1px solid #eee; }
        .passed { background: #d4edda; }
        .failed { background: #f8d7da; }
        .skipped { background: #e7e7e7; }
    </style>
</head>
<body>
    <h1>📊 تقرير الاختبارات</h1>
    <div class="summary">
        <h2>الملخص</h2>
        <p>✅ نجح: ${report.summary.passed}</p>
        <p>❌ فشل: ${report.summary.failed}</p>
        <p>⏭️ تخطي: ${report.summary.skipped}</p>
        <p>⏱️ الوقت: ${report.summary.time}ms</p>
    </div>`;

        for (const suite of report.suites) {
            html += `
    <div class="suite">
        <div class="suite-title">${suite.name}</div>`;

            for (const test of suite.tests) {
                const statusClass = test.status === 'passed' ? 'passed' : 
                                   test.status === 'failed' ? 'failed' : 'skipped';
                html += `
        <div class="test ${statusClass}">
            <strong>${test.name}</strong>
            <span>(${test.status}) ${test.duration}ms</span>
            ${test.error ? `<br><small>${test.error}</small>` : ''}
        </div>`;
            }

            html += `
    </div>`;
        }

        html += `
</body>
</html>`;

        return html;
    }

    /**
     * مسح النتائج
     */
    reset() {
        this.suites = [];
        this.results = {
            totalSuites: 0,
            totalTests: 0,
            passed: 0,
            failed: 0,
            skipped: 0,
            time: 0
        };
    }
}

// ==========================================
// أمثلة على الاستخدام
// ==========================================

const tester = new TestRunner();

/*

// مثال 1: اختبار محرك البلياردو
tester.describe('BilliardsEngine', () => {
    tester.test('حساب العصا يعمل', () => {
        const engine = new BilliardsEngine();
        const result = engine.calculateCue(3, 2);
        tester.equal(result, 5, 'يجب أن يكون 3 + 2 = 5');
    });

    tester.test('التحقق من القياس يعمل', () => {
        const engine = new BilliardsEngine();
        const valid = engine.validateMeasurement(3, 2, 5);
        tester.assert(valid, 'يجب أن يكون القياس صحيح');
    });

    tester.skip('اختبار معطل', () => {
        // هذا الاختبار سيتم تخطيه
    });
});

// مثال 2: اختبار خدمة التخزين
tester.describe('StorageService', () => {
    tester.test('الحفظ والتحميل يعمل', () => {
        const data = { test: 'value' };
        StorageService.save('test', data);
        const loaded = StorageService.load('test');
        tester.deepEqual(loaded, data, 'يجب تحميل نفس البيانات');
    });

    tester.test('الحذف يعمل', () => {
        StorageService.save('test', { value: 123 });
        StorageService.delete('test');
        const loaded = StorageService.load('test');
        tester.assert(loaded === null, 'يجب أن تكون البيانات محذوفة');
    });
});

// تشغيل الاختبارات
tester.run().then(results => {
    console.log('تم الانتهاء من الاختبارات');
});

// الحصول على تقرير مفصل
const report = tester.getDetailedReport();
console.log(report);

// تصدير النتائج
const html = tester.exportHTML();
// حفظ في ملف HTML

*/
