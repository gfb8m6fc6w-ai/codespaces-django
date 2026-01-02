// ==========================================
// السكريبت الرئيسي للتطبيق
// ==========================================

class BilliardsApp {
    constructor() {
        this.shots = [];
        this.calculator = new ShotCalculator();
        this.db = new DataManager();
        this.init();
    }
    
    async init() {
        console.log('تهيئة تطبيق البلياردو...');
        
        // تحميل البيانات
        await this.loadShots();
        
        // تسجيل Service Worker
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/service-worker.js')
                .then(reg => console.log('✓ Service Worker مسجل'))
                .catch(err => console.error('✗ خطأ في تسجيل Service Worker:', err));
        }
        
        // ربط الأحداث
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // زر الحساب
        const calcBtn = document.getElementById('calculate-btn');
        if (calcBtn) {
            calcBtn.addEventListener('click', () => this.calculateShot());
        }
        
        // التبويبات
        const tabBtns = document.querySelectorAll('.tab-btn');
        tabBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });
    }
    
    calculateShot() {
        try {
            const angle = parseFloat(document.getElementById('angle').value) || 0;
            const power = parseFloat(document.getElementById('power').value) || 50;
            const distance = parseFloat(document.getElementById('distance').value) || 100;
            const difficulty = parseInt(document.getElementById('difficulty').value) || 2;
            
            const result = this.calculator.calculate(angle, power, distance, difficulty);
            
            // حفظ التسديقة
            const shot = {
                angle,
                power,
                distance,
                difficulty,
                result,
                timestamp: new Date().toISOString()
            };
            
            this.shots.push(shot);
            this.db.saveShot(shot);
            
            // عرض النتيجة
            this.displayResult(result);
            
        } catch (error) {
            console.error('خطأ في الحساب:', error);
            alert('حدث خطأ في الحساب');
        }
    }
    
    displayResult(result) {
        const resultDiv = document.getElementById('result');
        if (resultDiv) {
            resultDiv.innerHTML = `
                <div class="card">
                    <div class="card-header">النتيجة</div>
                    <div class="card-body">
                        <p>نسبة النجاح: <strong>${result.successRate.toFixed(1)}%</strong></p>
                        <p>الصعوبة: <strong>${result.difficultyLabel}</strong></p>
                        <p>التوصية: ${result.recommendation}</p>
                    </div>
                </div>
            `;
        }
    }
    
    async loadShots() {
        this.shots = await this.db.loadShots();
        console.log(`تم تحميل ${this.shots.length} تسديقة`);
    }
    
    switchTab(tabName) {
        // إخفاء جميع التبويبات
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // إظهار التبويب المختار
        const activeTab = document.getElementById(`tab-${tabName}`);
        if (activeTab) {
            activeTab.classList.add('active');
        }
        
        // تحديث أزرار التبويبات
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });
    }
    
    getStatistics() {
        if (this.shots.length === 0) {
            return {
                total: 0,
                avgSuccess: 0,
                best: null,
                worst: null
            };
        }
        
        const successRates = this.shots.map(s => s.result.successRate);
        
        return {
            total: this.shots.length,
            avgSuccess: (successRates.reduce((a, b) => a + b, 0) / successRates.length).toFixed(1),
            best: Math.max(...successRates).toFixed(1),
            worst: Math.min(...successRates).toFixed(1)
        };
    }
}

// ==========================================
// حاسبة التسديقات
// ==========================================

class ShotCalculator {
    constructor() {
        this.difficultyLevels = [
            'سهل جداً',
            'سهل',
            'متوسط',
            'صعب',
            'صعب جداً',
            'احترافي'
        ];
    }
    
    calculate(angle, power, distance, difficulty) {
        // حساب عوامل مختلفة
        const angleFactor = this.calculateAngleFactor(angle);
        const powerFactor = this.calculatePowerFactor(power);
        const distanceFactor = this.calculateDistanceFactor(distance);
        const difficultyFactor = this.calculateDifficultyFactor(difficulty);
        
        // الحساب النهائي
        const successRate = (
            angleFactor * 0.25 +
            powerFactor * 0.25 +
            distanceFactor * 0.25 +
            difficultyFactor * 0.25
        );
        
        return {
            successRate: Math.max(0, Math.min(100, successRate)),
            angleFactor,
            powerFactor,
            distanceFactor,
            difficultyFactor,
            difficultyLabel: this.difficultyLevels[difficulty] || 'غير محدد',
            recommendation: this.getRecommendation(angle, power, distance)
        };
    }
    
    calculateAngleFactor(angle) {
        const penalty = Math.abs(angle) / 90 * 50;
        return 100 - penalty;
    }
    
    calculatePowerFactor(power) {
        if (power < 0 || power > 100) return 0;
        
        if (power >= 40 && power <= 70) return 100;
        if (power >= 20 && power < 40) return 60 + (power - 20) * 2;
        if (power > 70 && power <= 100) return 100 - (power - 70) * 1.5;
        
        return power;
    }
    
    calculateDistanceFactor(distance) {
        if (distance <= 50) return 100;
        if (distance <= 200) return 100 - (distance - 50) * 0.25;
        return 100 - (distance - 200) * 0.1;
    }
    
    calculateDifficultyFactor(difficulty) {
        const factors = [150, 120, 100, 80, 60, 40];
        return factors[difficulty] || 100;
    }
    
    getRecommendation(angle, power, distance) {
        if (angle === 0) {
            return '✓ الزاوية مثالية';
        } else if (Math.abs(angle) < 30) {
            return '○ حاول تقليل الزاوية';
        } else {
            return '⚠ اخفض الزاوية أكثر';
        }
    }
}

// ==========================================
// مدير البيانات
// ==========================================

class DataManager {
    constructor() {
        this.storageKey = 'billiardsApp_shots';
    }
    
    async saveShot(shot) {
        try {
            const shots = await this.loadShots();
            shots.push(shot);
            localStorage.setItem(this.storageKey, JSON.stringify(shots));
            return true;
        } catch (error) {
            console.error('خطأ في حفظ البيانات:', error);
            return false;
        }
    }
    
    async loadShots() {
        try {
            const data = localStorage.getItem(this.storageKey);
            return data ? JSON.parse(data) : [];
        } catch (error) {
            console.error('خطأ في تحميل البيانات:', error);
            return [];
        }
    }
    
    async clearShots() {
        try {
            localStorage.removeItem(this.storageKey);
            return true;
        } catch (error) {
            console.error('خطأ في مسح البيانات:', error);
            return false;
        }
    }
}

// ==========================================
// بدء التطبيق
// ==========================================

document.addEventListener('DOMContentLoaded', () => {
    window.app = new BilliardsApp();
});

// تدعم PWA
if ('serviceWorker' in navigator) {
    window.addEventListener('beforeinstallprompt', (e) => {
        console.log('التطبيق جاهز للتثبيت');
    });
}
