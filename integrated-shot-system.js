// 📁 integrated-shot-system.js
// نظام متكامل للعبة البلياردو مع دعم جميع الأنظمة

/**
 * فئة النظام المتكامل الرئيسية
 */
class IntegratedBilliardsSystem {
    constructor() {
        // مكونات النظام
        this.railsSystem = new RailPositionsSystem();
        this.shotDataManager = new ShotDataManager();
        this.shotPathCalculator = new ShotPathCalculator(this.railsSystem);
        this.geometryCalculator = new GeometryCalculator();
        this.tableStateManager = null;
        
        // الحالة الحالية
        this.currentShot = null;
        this.currentRails = 3;
        this.library = [];
        this.statistics = {
            totalShots: 0,
            successfulShots: 0,
            difficultShotsAttempted: 0,
            averageDifficulty: 0
        };
        
        // تحميل البيانات
        this.loadFromStorage();
        
        console.log('✅ نظام البلياردو المتكامل جاهز');
    }

    /**
     * بدء تطبيق جديد
     */
    initialize() {
        this.setupUI();
        this.setupEventListeners();
        this.renderCurrentState();
    }

    /**
     * إعداد الواجهة المستخدمة
     */
    setupUI() {
        // إنشاء عناصر الواجهة الرئيسية
        if (!document.getElementById('billiards-container')) {
            const container = document.createElement('div');
            container.id = 'billiards-container';
            container.className = 'billiards-main-container';
            document.body.appendChild(container);
        }

        this.renderRailSelector();
        this.renderWhiteBallSelector();
        this.renderTargetSelector();
        this.renderCueSelector();
        this.renderResultsPanel();
        this.renderLibraryPanel();
    }

    /**
     * رسم محدد الجدران
     */
    renderRailSelector() {
        const container = document.getElementById('rail-selector-container') || 
                         this.createContainer('rail-selector-container', 'محدد الجدران');
        
        container.innerHTML = '';
        [1, 2, 3, 4].forEach(rails => {
            const btn = document.createElement('button');
            btn.className = `rail-btn ${rails === this.currentRails ? 'active' : ''}`;
            btn.textContent = `${rails} جدار`;
            btn.dataset.rails = rails;
            btn.addEventListener('click', () => this.selectRails(rails));
            container.appendChild(btn);
        });
    }

    /**
     * رسم محدد الكرة البيضاء
     */
    renderWhiteBallSelector() {
        const container = document.getElementById('white-ball-selector-container') || 
                         this.createContainer('white-ball-selector-container', 'موقع الكرة البيضاء');
        
        const positions = this.railsSystem.getAllWhiteBallPositions('long');
        container.innerHTML = '';
        
        // شريط تمرير
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.min = '0';
        slider.max = positions.length - 1;
        slider.className = 'position-slider';
        slider.addEventListener('input', (e) => {
            const value = positions[parseInt(e.target.value)];
            this.selectWhiteBallPosition(value);
        });
        
        // قائمة الاختيار
        const select = document.createElement('select');
        select.className = 'position-select';
        positions.forEach(pos => {
            const option = document.createElement('option');
            option.value = pos;
            option.textContent = `${pos} قدم`;
            select.appendChild(option);
        });
        select.addEventListener('change', (e) => {
            this.selectWhiteBallPosition(parseFloat(e.target.value));
        });
        
        container.appendChild(slider);
        container.appendChild(select);
    }

    /**
     * رسم محدد الهدف
     */
    renderTargetSelector() {
        const container = document.getElementById('target-selector-container') || 
                         this.createContainer('target-selector-container', 'موقع الهدف');
        
        const positions = this.railsSystem.getAllTargetPositions('long');
        container.innerHTML = '';
        
        // شريط تمرير
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.min = '0';
        slider.max = positions.length - 1;
        slider.className = 'position-slider';
        slider.addEventListener('input', (e) => {
            const value = positions[parseInt(e.target.value)];
            this.selectTarget(value);
        });
        
        // قائمة الاختيار
        const select = document.createElement('select');
        select.className = 'position-select';
        positions.forEach(pos => {
            const option = document.createElement('option');
            option.value = pos;
            option.textContent = `${pos} قدم`;
            select.appendChild(option);
        });
        select.addEventListener('change', (e) => {
            this.selectTarget(parseFloat(e.target.value));
        });
        
        container.appendChild(slider);
        container.appendChild(select);
    }

    /**
     * رسم محدد قياس العصا
     */
    renderCueSelector() {
        const container = document.getElementById('cue-selector-container') || 
                         this.createContainer('cue-selector-container', 'قياس العصا');
        
        container.innerHTML = '';
        
        // شريط التمرير
        const slider = document.createElement('input');
        slider.type = 'range';
        slider.min = '0';
        slider.max = '20';
        slider.step = '0.5';
        slider.className = 'cue-slider';
        slider.addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            this.selectCueMeasurement(value);
            displayValue.textContent = value.toFixed(1);
        });
        
        const displayValue = document.createElement('span');
        displayValue.className = 'cue-display';
        displayValue.textContent = '0.0';
        
        container.appendChild(slider);
        container.appendChild(displayValue);
    }

    /**
     * رسم لوحة النتائج
     */
    renderResultsPanel() {
        const container = document.getElementById('results-panel') || 
                         this.createContainer('results-panel', 'النتائج');
        
        container.innerHTML = `
            <div class="result-item">
                <label>درجة الصعوبة:</label>
                <span id="difficulty-score">0</span>%
            </div>
            <div class="result-item">
                <label>عدد الجدران:</label>
                <span id="rails-count">3</span>
            </div>
            <div class="result-item">
                <label>موقع الكرة البيضاء:</label>
                <span id="white-ball-display">-</span> قدم
            </div>
            <div class="result-item">
                <label>موقع الهدف:</label>
                <span id="target-display">-</span> قدم
            </div>
            <div class="result-item">
                <label>قياس العصا:</label>
                <span id="cue-display">-</span>
            </div>
            <div class="result-item">
                <label>نوع الدوران:</label>
                <select id="spin-type">
                    <option value="none">بلا دوران</option>
                    <option value="topspin">دوران أمامي</option>
                    <option value="backspin">دوران خلفي</option>
                    <option value="english">إنجليزي</option>
                </select>
            </div>
            <button id="save-shot-btn" class="action-btn">حفظ اللقطة</button>
            <button id="calculate-path-btn" class="action-btn">حساب المسار</button>
        `;
        
        document.getElementById('save-shot-btn').addEventListener('click', () => this.saveCurrentShot());
        document.getElementById('calculate-path-btn').addEventListener('click', () => this.calculateShotPath());
    }

    /**
     * رسم لوحة المكتبة
     */
    renderLibraryPanel() {
        const container = document.getElementById('library-panel') || 
                         this.createContainer('library-panel', 'مكتبة اللقطات');
        
        container.innerHTML = `
            <div class="library-stats">
                <p>إجمالي اللقطات: <strong id="total-shots">0</strong></p>
                <p>نسبة النجاح: <strong id="success-rate">0%</strong></p>
                <p>متوسط الصعوبة: <strong id="avg-difficulty">0%</strong></p>
            </div>
            <div id="shots-list" class="shots-list">
                <p class="empty-message">لا توجد لقطات محفوظة</p>
            </div>
        `;
        
        this.updateLibraryDisplay();
    }

    /**
     * إنشاء حاوية مع عنوان
     */
    createContainer(id, title) {
        const container = document.createElement('div');
        container.id = id;
        container.className = 'panel-container';
        
        const titleElem = document.createElement('h3');
        titleElem.textContent = title;
        
        container.appendChild(titleElem);
        
        const content = document.createElement('div');
        content.className = 'panel-content';
        container.appendChild(content);
        
        document.getElementById('billiards-container').appendChild(container);
        
        return content;
    }

    /**
     * اختيار عدد الجدران
     */
    selectRails(rails) {
        this.currentRails = rails;
        this.renderRailSelector();
        this.updateCurrentShot();
    }

    /**
     * اختيار موقع الكرة البيضاء
     */
    selectWhiteBallPosition(position) {
        if (!this.currentShot) {
            this.currentShot = this.shotDataManager.createShot();
        }
        this.currentShot.whiteBallMeasurement = position;
        this.updateCurrentShot();
    }

    /**
     * اختيار موقع الهدف
     */
    selectTarget(position) {
        if (!this.currentShot) {
            this.currentShot = this.shotDataManager.createShot();
        }
        this.currentShot.targetMeasurement = position;
        this.updateCurrentShot();
    }

    /**
     * اختيار قياس العصا
     */
    selectCueMeasurement(measurement) {
        if (!this.currentShot) {
            this.currentShot = this.shotDataManager.createShot();
        }
        this.currentShot.cueMeasurement = measurement;
        this.updateCurrentShot();
    }

    /**
     * تحديث حالة اللقطة الحالية
     */
    updateCurrentShot() {
        if (!this.currentShot) {
            this.currentShot = this.shotDataManager.createShot({
                rails: this.currentRails
            });
        }
        
        this.currentShot.rails = this.currentRails;
        this.currentShot.difficulty = this.shotDataManager.calculateDifficulty(this.currentShot);
        
        // تحديث الواجهة
        this.updateResultsDisplay();
    }

    /**
     * تحديث عرض النتائج
     */
    updateResultsDisplay() {
        if (!this.currentShot) return;
        
        document.getElementById('difficulty-score').textContent = 
            Math.round(this.currentShot.difficulty);
        document.getElementById('rails-count').textContent = this.currentShot.rails;
        document.getElementById('white-ball-display').textContent = 
            this.currentShot.whiteBallMeasurement || '-';
        document.getElementById('target-display').textContent = 
            this.currentShot.targetMeasurement || '-';
        document.getElementById('cue-display').textContent = 
            this.currentShot.cueMeasurement?.toFixed(1) || '-';
    }

    /**
     * حساب مسار اللقطة
     */
    calculateShotPath() {
        if (!this.currentShot || !this.currentShot.whiteBallMeasurement || !this.currentShot.targetMeasurement) {
            alert('يرجى إدخال جميع القياسات');
            return;
        }

        let pathData;
        
        switch(this.currentShot.rails) {
            case 1:
                pathData = this.shotPathCalculator.calculateOneRailPath(this.currentShot);
                break;
            case 2:
                pathData = this.shotPathCalculator.calculateTwoRailsPath(this.currentShot);
                break;
            case 3:
                pathData = this.shotPathCalculator.calculateThreeRailsPath(this.currentShot);
                break;
            case 4:
                pathData = this.shotPathCalculator.calculateFourRailsPath(this.currentShot);
                break;
            default:
                return;
        }

        // حفظ بيانات المسار
        this.currentShot.pathData = pathData;
        
        // عرض المسار بصرياً
        this.visualizePath(pathData);
        
        alert(`تم حساب مسار بـ ${this.currentShot.rails} جدران\nصعوبة: ${Math.round(this.currentShot.difficulty)}%`);
    }

    /**
     * عرض المسار بصرياً
     */
    visualizePath(pathData) {
        // هذا يمكن تطويره لعرض رسم بياني للمسار
        console.log('مسار اللقطة:', pathData);
    }

    /**
     * حفظ اللقطة الحالية
     */
    saveCurrentShot() {
        if (!this.currentShot) {
            alert('لا توجد لقطة حالية لحفظها');
            return;
        }

        const result = this.shotDataManager.saveShot(this.currentShot);
        
        if (result.success) {
            // إضافة إلى المكتبة
            this.library.unshift(this.currentShot);
            this.updateStatistics();
            this.updateLibraryDisplay();
            this.saveToStorage();
            
            alert('تم حفظ اللقطة بنجاح!');
            
            // إعادة تعيين
            this.currentShot = null;
            this.updateResultsDisplay();
        } else {
            alert('خطأ: ' + result.errors.join('\n'));
        }
    }

    /**
     * تحديث الإحصائيات
     */
    updateStatistics() {
        this.statistics.totalShots = this.library.length;
        this.statistics.difficultShotsAttempted = this.library.filter(s => s.difficulty > 70).length;
        
        if (this.library.length > 0) {
            const totalDifficulty = this.library.reduce((sum, shot) => sum + shot.difficulty, 0);
            this.statistics.averageDifficulty = totalDifficulty / this.library.length;
        }
    }

    /**
     * تحديث عرض المكتبة
     */
    updateLibraryDisplay() {
        const list = document.getElementById('shots-list');
        
        if (this.library.length === 0) {
            list.innerHTML = '<p class="empty-message">لا توجد لقطات محفوظة</p>';
            return;
        }

        list.innerHTML = this.library.map((shot, index) => `
            <div class="shot-card">
                <div class="shot-header">
                    <h4>لقطة #${index + 1}</h4>
                    <span class="shot-difficulty" style="color: ${shot.difficulty > 70 ? 'red' : 'green'}">
                        ${Math.round(shot.difficulty)}%
                    </span>
                </div>
                <p><strong>الجدران:</strong> ${shot.rails}</p>
                <p><strong>الكرة البيضاء:</strong> ${shot.whiteBallMeasurement} قدم</p>
                <p><strong>الهدف:</strong> ${shot.targetMeasurement} قدم</p>
                <p><strong>العصا:</strong> ${shot.cueMeasurement.toFixed(1)}</p>
                <button class="delete-btn" onclick="window.billiards.deleteShot(${shot.id})">حذف</button>
            </div>
        `).join('');

        // تحديث الإحصائيات
        document.getElementById('total-shots').textContent = this.library.length;
        document.getElementById('avg-difficulty').textContent = 
            Math.round(this.statistics.averageDifficulty) + '%';
    }

    /**
     * حذف لقطة
     */
    deleteShot(shotId) {
        this.library = this.library.filter(shot => shot.id !== shotId);
        this.shotDataManager.deleteShot(shotId);
        this.updateStatistics();
        this.updateLibraryDisplay();
        this.saveToStorage();
    }

    /**
     * إعداد مستمعي الأحداث
     */
    setupEventListeners() {
        // يمكن إضافة المزيد من مستمعي الأحداث هنا
    }

    /**
     * تحديث الحالة الحالية للعرض
     */
    renderCurrentState() {
        this.updateResultsDisplay();
        this.updateLibraryDisplay();
    }

    /**
     * حفظ في التخزين المحلي
     */
    saveToStorage() {
        try {
            localStorage.setItem('billiardsShotLibrary', JSON.stringify(this.library));
            localStorage.setItem('billiardStatistics', JSON.stringify(this.statistics));
        } catch (e) {
            console.warn('خطأ في حفظ البيانات:', e);
        }
    }

    /**
     * تحميل من التخزين المحلي
     */
    loadFromStorage() {
        try {
            const savedLibrary = localStorage.getItem('billiardsShotLibrary');
            if (savedLibrary) {
                this.library = JSON.parse(savedLibrary);
            }

            const savedStats = localStorage.getItem('billiardStatistics');
            if (savedStats) {
                this.statistics = JSON.parse(savedStats);
            }
        } catch (e) {
            console.warn('خطأ في قراءة البيانات:', e);
        }
    }
}

// إنشاء مثيل عام
const billiards = new IntegratedBilliardsSystem();

// تصدير للاستخدام
if (typeof module !== 'undefined' && module.exports) {
    module.exports = IntegratedBilliardsSystem;
}
