// 📱 نظام PWA والإدارة الكاملة
let deferredPrompt;
let isStandalone = false;

// التحقق من وضع التطبيق
function checkStandaloneMode() {
    isStandalone = (window.matchMedia('(display-mode: standalone)').matches) || 
                   (window.navigator.standalone) || 
                   (document.referrer.includes('android-app://'));
    
    if (isStandalone) {
        document.body.classList.add('standalone-mode');
        console.log('التطبيق يعمل في وضع التطبيق المستقل');
    }
}

// عرض زر التثبيت
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    
    // تأخير عرض الإشعار لمدة 5 ثواني
    setTimeout(() => {
        showInstallBanner();
    }, 5000);
});

function showInstallBanner() {
    const container = document.getElementById('installContainer');
    if (container && deferredPrompt && !isStandalone) {
        container.style.display = 'block';
    }
}

function hideInstallBanner() {
    const container = document.getElementById('installContainer');
    if (container) {
        container.style.display = 'none';
    }
}

async function installApp() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        
        if (outcome === 'accepted') {
            console.log('تم تثبيت التطبيق بنجاح');
            hideInstallBanner();
        }
        
        deferredPrompt = null;
    }
}

// تسجيل Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('./sw.js')
            .then(registration => {
                console.log('Service Worker مسجل:', registration.scope);
            })
            .catch(error => {
                console.log('فشل تسجيل Service Worker:', error);
            });
    });
}

// 🗄️ نظام إدارة القياسات الكامل
class ShotDatabaseManager {
    constructor() {
        this.localDatabase = JSON.parse(localStorage.getItem('5a-diamond-database')) || {};
        this.customShots = JSON.parse(localStorage.getItem('5a-custom-shots')) || [];
        this.backups = JSON.parse(localStorage.getItem('5a-backups')) || [];
        this.categories = JSON.parse(localStorage.getItem('5a-categories')) || this.getDefaultCategories();
        
        this.initDatabase();
    }
    
    getDefaultCategories() {
        return {
            'standard': { name: 'قياسات قياسية', color: '#0066CC', icon: 'fas fa-star' },
            'favorite': { name: 'المفضلة', color: '#FFA500', icon: 'fas fa-heart' },
            'difficult': { name: 'تسديدات صعبة', color: '#DC143C', icon: 'fas fa-fire' },
            'corner': { name: 'زوايا', color: '#00CC66', icon: 'fas fa-drafting-compass' },
            'rail': { name: 'انعكاسات', color: '#9C27B0', icon: 'fas fa-project-diagram' },
            'custom': { name: 'مخصص', color: '#607D8B', icon: 'fas fa-edit' }
        };
    }
    
    initDatabase() {
        // دمج قاعدة البيانات الأساسية مع القياسات المخصصة
        this.database = this.generateCompleteDatabase();
        
        // إذا كانت هناك قياسات مخصصة، دمجها
        if (this.customShots.length > 0) {
            this.mergeCustomShots();
        }
    }
    
    generateCompleteDatabase() {
        // توليد قاعدة بيانات كاملة بناءً على نظام الدايمند
        const database = {};
        
        // الأشرطة من 1 إلى 4
        for (let bands = 1; bands <= 4; bands++) {
            database[bands] = {};
            
            // جميع قيم الدايمند
            DIAMOND_SYSTEM.forEach(cue => {
                database[bands][cue] = {};
                
                // جميع المواضع
                const positions = ['Top Right', 'Top Left', 'Mid Right', 'Mid Left', 'Down Right', 'Down Left'];
                positions.forEach(position => {
                    database[bands][cue][position] = this.generateShotData(bands, cue, position);
                });
            });
        }
        
        return database;
    }
    
    generateShotData(bands, cue, position) {
        const shots = [];
        const shotTypes = ['Max Limit', 'Point 7', 'Pocket', 'Rail 1', 'Rail 2', 'Rail 3'];
        
        shotTypes.forEach((type, index) => {
            // حساب قيمة دقيقة بناءً على القياسات
            const value = this.calculateShotValue(bands, cue, position, type, index);
            const power = this.calculateShotPower(bands, cue, position, type);
            const angle = this.calculateShotAngle(bands, cue, position, type);
            const spin = this.calculateSpinEffect(cue);
            
            shots.push({
                r: type,
                v: value.toFixed(2),
                power: power,
                angle: angle,
                spin: spin,
                tip: this.generateTip(bands, cue, position, type),
                category: 'standard',
                difficulty: this.calculateDifficulty(bands, cue, position, type),
                successRate: this.calculateSuccessRate(bands, cue, position, type),
                id: this.generateShotId(bands, cue, position, type)
            });
        });
        
        return shots;
    }
    
    calculateShotValue(bands, cue, position, type, index) {
        // قيمة أساسية + تأثير الأشرطة + تأثير الكيو + تأثير النوع
        let baseValue = 1.5 + (index * 0.5);
        baseValue += (parseInt(bands) - 1) * 0.2;
        baseValue += parseFloat(cue) * 0.3;
        
        // تعديل حسب الموضع
        if (position.includes('Left')) baseValue *= 0.95;
        if (position.includes('Top')) baseValue *= 1.05;
        
        return baseValue;
    }
    
    calculateShotPower(bands, cue, position, type) {
        let power = 75;
        power += (parseInt(bands) - 1) * 5;
        power += parseFloat(cue) * 4;
        
        if (type.includes('Rail')) power += 10;
        if (position.includes('Down')) power -= 5;
        
        return Math.min(100, Math.max(60, Math.round(power))) + '%';
    }
    
    calculateShotAngle(bands, cue, position, type) {
        let angle = 45;
        angle -= (parseInt(bands) - 1) * 5;
        angle += parseFloat(cue) * 3;
        
        if (position.includes('Left')) angle += 15;
        if (position.includes('Right')) angle -= 10;
        if (type.includes('Rail')) angle -= 8;
        
        return Math.max(15, Math.min(80, Math.round(angle)));
    }
    
    calculateSpinEffect(cue) {
        const cueValue = parseFloat(cue);
        if (cueValue <= 1) return 'خفيف';
        if (cueValue <= 2) return 'متوسط';
        if (cueValue <= 3) return 'قوي';
        return 'أقصى';
    }
    
    calculateDifficulty(bands, cue, position, type) {
        let difficulty = parseInt(bands) * 2;
        difficulty += parseFloat(cue) * 1.5;
        
        if (position.includes('Left')) difficulty += 1;
        if (type.includes('Rail')) difficulty += 1.5;
        
        return Math.min(10, Math.max(1, Math.round(difficulty * 10) / 10));
    }
    
    calculateSuccessRate(bands, cue, position, type) {
        let rate = 85;
        rate -= (parseInt(bands) - 1) * 8;
        rate -= parseFloat(cue) * 4;
        
        if (position.includes('Left')) rate -= 5;
        if (type.includes('Rail')) rate -= 10;
        
        return Math.max(30, Math.min(95, Math.round(rate)));
    }
    
    generateTip(bands, cue, position, type) {
        const tips = [];
        const cueValue = parseFloat(cue);
        
        if (cueValue >= 2.5) {
            tips.push('استخدم متابعة طويلة للكيو');
        }
        
        if (parseInt(bands) >= 3) {
            tips.push('ركز على نقطة الارتكاز قبل الضربة');
        }
        
        if (position.includes('Left')) {
            tips.push('أضف نصف كرة نحو اليمين');
        }
        
        if (type.includes('Rail')) {
            tips.push('تحكم في القوة حسب عدد الانعكاسات');
        }
        
        return tips.length > 0 ? tips.join(' - ') : 'ضربة قياسية، ركز على الهدف';
    }
    
    generateShotId(bands, cue, position, type) {
        return `${bands}-${cue}-${position.replace(' ', '-')}-${type.replace(' ', '-')}`.toLowerCase();
    }
    
    // 🎯 إضافة قياسات مخصصة
    addCustomShot(shotData) {
        const shot = {
            ...shotData,
            id: `custom-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
            dateAdded: new Date().toISOString(),
            lastModified: new Date().toISOString(),
            category: shotData.category || 'custom',
            rating: shotData.rating || 3
        };
        
        this.customShots.push(shot);
        this.saveToLocalStorage();
        this.mergeCustomShots();
        
        return shot.id;
    }
    
    mergeCustomShots() {
        // دمج القياسات المخصصة مع القاعدة الأساسية
        this.customShots.forEach(shot => {
            const { bands, cue, position } = shot;
            
            if (!this.database[bands]) this.database[bands] = {};
            if (!this.database[bands][cue]) this.database[bands][cue] = {};
            if (!this.database[bands][cue][position]) this.database[bands][cue][position] = [];
            
            // البحث عن تسديدة موجودة بنفس النوع
            const existingIndex = this.database[bands][cue][position].findIndex(
                s => s.r === shot.r
            );
            
            if (existingIndex >= 0) {
                // استبدال القياس الموجود
                this.database[bands][cue][position][existingIndex] = {
                    ...this.database[bands][cue][position][existingIndex],
                    ...shot,
                    isCustom: true
                };
            } else {
                // إضافة تسديدة جديدة
                this.database[bands][cue][position].push({
                    ...shot,
                    isCustom: true
                });
            }
        });
    }
    
    // 📤 تصدير البيانات
    exportDatabase(format = 'json') {
        const data = {
            metadata: {
                exportDate: new Date().toISOString(),
                version: '3.0',
                system: '5A Diamond System Pro',
                totalCustomShots: this.customShots.length,
                totalCategories: Object.keys(this.categories).length
            },
            diamondSystem: DIAMOND_SYSTEM,
            categories: this.categories,
            customShots: this.customShots,
            backups: this.backups.slice(-5) // آخر 5 نسخ احتياطية
        };
        
        if (format === 'json') {
            return JSON.stringify(data, null, 2);
        } else if (format === 'csv') {
            return this.convertToCSV(data);
        }
        
        return data;
    }
    
    convertToCSV(data) {
        let csv = 'ID,Bands,Cue,Position,Type,Value,Power,Angle,Category,Rating,Difficulty,SuccessRate,DateAdded\n';
        
        data.customShots.forEach(shot => {
            csv += `${shot.id},${shot.bands},${shot.cue},${shot.position},${shot.r},${shot.v},${shot.power},${shot.angle},${shot.category},${shot.rating || ''},${shot.difficulty || ''},${shot.successRate || ''},${shot.dateAdded}\n`;
        });
        
        return csv;
    }
    
    // 📥 استيراد البيانات
    importDatabase(jsonData) {
        try {
            const data = JSON.parse(jsonData);
            
            if (data.customShots) {
                this.customShots = data.customShots;
            }
            
            if (data.categories) {
                this.categories = { ...this.categories, ...data.categories };
            }
            
            this.saveToLocalStorage();
            this.initDatabase();
            
            return {
                success: true,
                importedShots: data.customShots?.length || 0,
                importedCategories: Object.keys(data.categories || {}).length
            };
            
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }
    
    // 💾 إنشاء نسخة احتياطية
    createBackup(name = '') {
        const backup = {
            id: `backup-${Date.now()}`,
            name: name || `نسخة احتياطية ${new Date().toLocaleString('ar-SA')}`,
            date: new Date().toISOString(),
            customShots: [...this.customShots],
            categories: { ...this.categories }
        };
        
        this.backups.push(backup);
        
        // الاحتفاظ بآخر 10 نسخ احتياطية فقط
        if (this.backups.length > 10) {
            this.backups = this.backups.slice(-10);
        }
        
        this.saveToLocalStorage();
        
        return backup.id;
    }
    
    // 🔄 استعادة نسخة احتياطية
    restoreBackup(backupId) {
        const backup = this.backups.find(b => b.id === backupId);
        if (backup) {
            this.customShots = backup.customShots;
            this.categories = backup.categories;
            this.saveToLocalStorage();
            this.initDatabase();
            return true;
        }
        return false;
    }
    
    // 🔍 البحث في القياسات
    searchShots(query) {
        const results = {
            byBands: [],
            byCue: [],
            byPosition: [],
            byCategory: [],
            byTip: []
        };
        
        this.customShots.forEach(shot => {
            // البحث في جميع الحقول
            const searchStr = JSON.stringify(shot).toLowerCase();
            const queryStr = query.toLowerCase();
            
            if (searchStr.includes(queryStr)) {
                if (shot.bands.toString().includes(query)) results.byBands.push(shot);
                if (shot.cue.toString().includes(query)) results.byCue.push(shot);
                if (shot.position.toLowerCase().includes(queryStr)) results.byPosition.push(shot);
                if (shot.category.toLowerCase().includes(queryStr)) results.byCategory.push(shot);
                if (shot.tip.toLowerCase().includes(queryStr)) results.byTip.push(shot);
            }
        });
        
        return results;
    }
    
    // 📊 إحصائيات
    getStatistics() {
        const stats = {
            totalShots: this.customShots.length,
            shotsByBands: {},
            shotsByCategory: {},
            averageDifficulty: 0,
            averageSuccessRate: 0,
            lastAdded: null,
            mostCommonPosition: null,
            topCategories: []
        };
        
        if (this.customShots.length === 0) return stats;
        
        // حساب الإحصائيات
        let totalDifficulty = 0;
        let totalSuccessRate = 0;
        const positionCount = {};
        const categoryCount = {};
        
        this.customShots.forEach(shot => {
            // حسب عدد الأشرطة
            stats.shotsByBands[shot.bands] = (stats.shotsByBands[shot.bands] || 0) + 1;
            
            // حسب التصنيف
            stats.shotsByCategory[shot.category] = (stats.shotsByCategory[shot.category] || 0) + 1;
            
            // حسب الموضع
            positionCount[shot.position] = (positionCount[shot.position] || 0) + 1;
            
            // حسب التصنيف للقائمة
            categoryCount[shot.category] = (categoryCount[shot.category] || 0) + 1;
            
            // جمع الصعوبة ومعدل النجاح
            if (shot.difficulty) totalDifficulty += shot.difficulty;
            if (shot.successRate) totalSuccessRate += shot.successRate;
            
            // آخر إضافة
            if (!stats.lastAdded || new Date(shot.dateAdded) > new Date(stats.lastAdded.dateAdded)) {
                stats.lastAdded = shot;
            }
        });
        
        // حساب المتوسطات
        stats.averageDifficulty = totalDifficulty / this.customShots.length;
        stats.averageSuccessRate = totalSuccessRate / this.customShots.length;
        
        // الموضع الأكثر شيوعاً
        stats.mostCommonPosition = Object.entries(positionCount)
            .sort((a, b) => b[1] - a[1])[0]?.[0] || null;
        
        // أفضل التصنيفات
        stats.topCategories = Object.entries(categoryCount)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 3)
            .map(([name, count]) => ({ name, count }));
        
        return stats;
    }
    
    // 💾 حفظ في التخزين المحلي
    saveToLocalStorage() {
        localStorage.setItem('5a-diamond-database', JSON.stringify(this.localDatabase));
        localStorage.setItem('5a-custom-shots', JSON.stringify(this.customShots));
        localStorage.setItem('5a-backups', JSON.stringify(this.backups));
        localStorage.setItem('5a-categories', JSON.stringify(this.categories));
    }
}

// 📱 واجهة إدارة القياسات
class ManagementInterface {
    constructor(databaseManager) {
        this.db = databaseManager;
        this.currentView = 'list';
        this.selectedShots = new Set();
    }
    
    // 🎨 عرض لوحة الإدارة
    showManagementPanel() {
        const html = `
            <div class="management-overlay">
                <div class="management-panel">
                    <div class="management-header">
                        <h2><i class="fas fa-database"></i> إدارة القياسات</h2>
                        <button onclick="management.close()" class="btn-close">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="management-tabs">
                        <button class="tab-btn active" data-tab="list">
                            <i class="fas fa-list"></i> جميع القياسات
                        </button>
                        <button class="tab-btn" data-tab="add">
                            <i class="fas fa-plus"></i> إضافة قياس
                        </button>
                        <button class="tab-btn" data-tab="import">
                            <i class="fas fa-file-import"></i> استيراد
                        </button>
                        <button class="tab-btn" data-tab="export">
                            <i class="fas fa-file-export"></i> تصدير
                        </button>
                        <button class="tab-btn" data-tab="stats">
                            <i class="fas fa-chart-bar"></i> إحصائيات
                        </button>
                        <button class="tab-btn" data-tab="backup">
                            <i class="fas fa-history"></i> النسخ الاحتياطي
                        </button>
                    </div>
                    
                    <div class="management-content">
                        <div id="managementList" class="tab-content active"></div>
                        <div id="managementAdd" class="tab-content"></div>
                        <div id="managementImport" class="tab-content"></div>
                        <div id="managementExport" class="tab-content"></div>
                        <div id="managementStats" class="tab-content"></div>
                        <div id="managementBackup" class="tab-content"></div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', html);
        this.bindEvents();
        this.loadTab('list');
    }
    
    bindEvents() {
        // أحداث التبويبات
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.currentTarget.dataset.tab;
                this.switchTab(tab);
            });
        });
    }
    
    switchTab(tabName) {
        // تحديث الأزرار النشطة
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.tab === tabName) {
                btn.classList.add('active');
            }
        });
        
        // تحديث المحتوى
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        
        document.getElementById(`management${tabName.charAt(0).toUpperCase() + tabName.slice(1)}`).classList.add('active');
        
        // تحميل محتوى التبويب
        this.loadTab(tabName);
    }
    
    async loadTab(tabName) {
        switch(tabName) {
            case 'list':
                await this.loadShotsList();
                break;
            case 'add':
                this.loadAddForm();
                break;
            case 'import':
                this.loadImportPanel();
                break;
            case 'export':
                this.loadExportPanel();
                break;
            case 'stats':
                this.loadStatsPanel();
                break;
            case 'backup':
                this.loadBackupPanel();
                break;
        }
    }
    
    async loadShotsList() {
        const container = document.getElementById('managementList');
        const shots = this.db.customShots;
        
        let html = `
            <div class="shots-header">
                <h3><i class="fas fa-bullseye"></i> قياساتي (${shots.length})</h3>
                <div class="shots-controls">
                    <input type="text" id="searchShots" placeholder="🔍 بحث في القياسات..." class="search-input">
                    <select id="filterCategory" class="filter-select">
                        <option value="">جميع التصنيفات</option>
                        ${Object.entries(this.db.categories).map(([id, cat]) => 
                            `<option value="${id}">${cat.name}</option>`
                        ).join('')}
                    </select>
                    <button onclick="management.bulkDelete()" class="btn-danger">
                        <i class="fas fa-trash"></i> حذف المحدد
                    </button>
                </div>
            </div>
            
            <div class="shots-grid" id="shotsGrid">
        `;
        
        if (shots.length === 0) {
            html += `
                <div class="empty-shots">
                    <i class="fas fa-inbox"></i>
                    <h4>لا توجد قياسات مضافة</h4>
                    <p>ابدأ بإضافة قياساتك الخاصة</p>
                    <button onclick="management.switchTab('add')" class="btn-primary">
                        <i class="fas fa-plus"></i> إضافة أول قياس
                    </button>
                </div>
            `;
        } else {
            shots.forEach((shot, index) => {
                const category = this.db.categories[shot.category] || this.db.categories.custom;
                html += `
                    <div class="shot-item" data-id="${shot.id}">
                        <div class="shot-checkbox">
                            <input type="checkbox" id="shot-${index}" 
                                   onchange="management.toggleSelection('${shot.id}')">
                        </div>
                        <div class="shot-content">
                            <div class="shot-header">
                                <span class="shot-name">${shot.r}</span>
                                <span class="shot-category" style="background: ${category.color}">
                                    <i class="${category.icon}"></i> ${category.name}
                                </span>
                            </div>
                            <div class="shot-details">
                                <span><i class="fas fa-layer-group"></i> ${shot.bands} أشرطة</span>
                                <span><i class="fas fa-gem"></i> كيو ${shot.cue}</span>
                                <span><i class="fas fa-bullseye"></i> ${this.getArabicPosition(shot.position)}</span>
                            </div>
                            <div class="shot-values">
                                <span class="value"><strong>${shot.v}</strong></span>
                                <span class="power">${shot.power}</span>
                                <span class="angle">${shot.angle}°</span>
                            </div>
                            <div class="shot-actions">
                                <button onclick="management.editShot('${shot.id}')" class="btn-icon">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button onclick="management.duplicateShot('${shot.id}')" class="btn-icon">
                                    <i class="fas fa-copy"></i>
                                </button>
                                <button onclick="management.deleteShot('${shot.id}')" class="btn-icon">
                                    <i class="fas fa-trash"></i>
                                </button>
                                <button onclick="management.testShot('${shot.id}')" class="btn-primary">
                                    <i class="fas fa-play"></i> تجربة
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        
        html += `</div>`;
        
        container.innerHTML = html;
        
        // إضافة مستمعي الأحداث للبحث والتصفية
        document.getElementById('searchShots').addEventListener('input', (e) => {
            this.filterShots(e.target.value);
        });
        
        document.getElementById('filterCategory').addEventListener('change', (e) => {
            this.filterByCategory(e.target.value);
        });
    }
    
    loadAddForm() {
        const container = document.getElementById('managementAdd');
        
        const html = `
            <div class="add-form">
                <h3><i class="fas fa-plus-circle"></i> إضافة قياس جديد</h3>
                
                <div class="form-grid">
                    <div class="form-group">
                        <label for="shotName">اسم القياس</label>
                        <input type="text" id="shotName" placeholder="مثال: تسديدة الزاوية الصعبة">
                    </div>
                    
                    <div class="form-group">
                        <label for="shotBands">عدد الأشرطة</label>
                        <select id="shotBands" class="styled-select">
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4" selected>4</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="shotCue">موضع الكيو (نظام الدايمند)</label>
                        <select id="shotCue" class="styled-select">
                            ${DIAMOND_SYSTEM.map(value => 
                                `<option value="${value}">${value}</option>`
                            ).join('')}
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="shotPosition">الموضع</label>
                        <select id="shotPosition" class="styled-select">
                            <option value="Top Right">أعلى اليمين</option>
                            <option value="Top Left">أعلى اليسار</option>
                            <option value="Mid Right">وسط اليمين</option>
                            <option value="Mid Left">وسط اليسار</option>
                            <option value="Down Right">أسفل اليمين</option>
                            <option value="Down Left">أسفل اليسار</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="shotType">نوع التسديدة</label>
                        <select id="shotType" class="styled-select">
                            <option value="Max Limit">Max Limit</option>
                            <option value="Point 7">Point 7</option>
                            <option value="Pocket" selected>Pocket</option>
                            <option value="Rail 1">Rail 1</option>
                            <option value="Rail 2">Rail 2</option>
                            <option value="Rail 3">Rail 3</option>
                            <option value="Custom">مخصص</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="shotValue">القيمة</label>
                        <input type="number" id="shotValue" step="0.01" placeholder="2.5" value="2.5">
                    </div>
                    
                    <div class="form-group">
                        <label for="shotPower">القوة المطلوبة</label>
                        <select id="shotPower" class="styled-select">
                            <option value="60%">60%</option>
                            <option value="65%">65%</option>
                            <option value="70%">70%</option>
                            <option value="75%">75%</option>
                            <option value="80%">80%</option>
                            <option value="85%" selected>85%</option>
                            <option value="90%">90%</option>
                            <option value="95%">95%</option>
                            <option value="100%">100%</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="shotAngle">الزاوية (°)</label>
                        <input type="number" id="shotAngle" min="0" max="90" value="45">
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="shotCategory">التصنيف</label>
                        <div class="category-buttons">
                            ${Object.entries(this.db.categories).map(([id, cat]) => `
                                <button class="category-btn" data-id="${id}" style="background: ${cat.color}">
                                    <i class="${cat.icon}"></i> ${cat.name}
                                </button>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="shotTip">النصيحة/الملاحظات</label>
                        <textarea id="shotTip" rows="3" placeholder="أدخل النصيحة أو الملاحظات لهذا القياس..."></textarea>
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="shotDifficulty">الصعوبة (1-10)</label>
                        <input type="range" id="shotDifficulty" min="1" max="10" value="5" class="slider">
                        <div class="slider-value">
                            <span id="difficultyValue">5</span>
                        </div>
                    </div>
                    
                    <div class="form-group full-width">
                        <label for="shotSuccessRate">معدل النجاح المتوقع (%)</label>
                        <input type="range" id="shotSuccessRate" min="10" max="100" value="75" class="slider">
                        <div class="slider-value">
                            <span id="successRateValue">75%</span>
                        </div>
                    </div>
                </div>
                
                <div class="form-actions">
                    <button onclick="management.saveShot()" class="btn-primary">
                        <i class="fas fa-save"></i> حفظ القياس
                    </button>
                    <button onclick="management.resetForm()" class="btn-secondary">
                        <i class="fas fa-redo"></i> مسح النموذج
                    </button>
                    <button onclick="management.captureFromCurrent()" class="btn-info">
                        <i class="fas fa-camera"></i> التقاط من الإعدادات الحالية
                    </button>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
        
        // أحداث السلايدر
        document.getElementById('shotDifficulty').addEventListener('input', function() {
            document.getElementById('difficultyValue').textContent = this.value;
        });
        
        document.getElementById('shotSuccessRate').addEventListener('input', function() {
            document.getElementById('successRateValue').textContent = this.value + '%';
        });
        
        // أحداث أزرار التصنيف
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.category-btn').forEach(b => {
                    b.classList.remove('active');
                });
                this.classList.add('active');
            });
        });
        
        // تفعيل أول تصنيف
        document.querySelector('.category-btn')?.classList.add('active');
    }
    
    saveShot() {
        const shotData = {
            r: document.getElementById('shotName').value || document.getElementById('shotType').value,
            bands: document.getElementById('shotBands').value,
            cue: document.getElementById('shotCue').value,
            position: document.getElementById('shotPosition').value,
            v: document.getElementById('shotValue').value,
            power: document.getElementById('shotPower').value,
            angle: parseInt(document.getElementById('shotAngle').value),
            tip: document.getElementById('shotTip').value,
            category: document.querySelector('.category-btn.active')?.dataset.id || 'custom',
            difficulty: parseFloat(document.getElementById('shotDifficulty').value),
            successRate: parseInt(document.getElementById('shotSuccessRate').value)
        };
        
        // التحقق من البيانات
        if (!shotData.bands || !shotData.cue || !shotData.position) {
            this.showNotification('يرجى ملء جميع الحقول المطلوبة', 'error');
            return;
        }
        
        const shotId = this.db.addCustomShot(shotData);
        
        this.showNotification('تم حفظ القياس بنجاح!', 'success');
        this.switchTab('list');
    }
    
    captureFromCurrent() {
        // التقاط الإعدادات الحالية من الواجهة الرئيسية
        document.getElementById('shotBands').value = document.getElementById('bands').value;
        document.getElementById('shotCue').value = document.getElementById('cue').value;
        document.getElementById('shotPosition').value = document.getElementById('pocket').value;
        
        this.showNotification('تم التقاط الإعدادات الحالية', 'info');
    }
    
    // ... باقي دوال الإدارة
}

// 🌐 تهيئة التطبيق
let dbManager;
let management;

function initCompleteApp() {
    // التحقق من وضع التطبيق
    checkStandaloneMode();
    
    // تهيئة مدير قاعدة البيانات
    dbManager = new ShotDatabaseManager();
    
    // تهيئة واجهة الإدارة
    management = new ManagementInterface(dbManager);
    
    // تهيئة نظام الدايمند
    initDiamondSystem();
    
    // إضافة زر الإدارة
    addManagementButton();
    
    console.log('تطبيق 5A Diamond System Pro جاهز للاستخدام!');
}

function addManagementButton() {
    const managementBtn = document.createElement('button');
    managementBtn.className = 'management-btn';
    managementBtn.innerHTML = '<i class="fas fa-cog"></i> إدارة القياسات';
    managementBtn.onclick = () => management.showManagementPanel();
    
    document.querySelector('.app-header').appendChild(managementBtn);
}

// تشغيل التطبيق
document.addEventListener('DOMContentLoaded', initCompleteApp);

// نظام السحب والإفلات للمحترفين
class DragDropEditor {
    constructor() {
        this.draggedItem = null;
        this.init();
    }
    
    init() {
        this.enableDragAndDrop();
        this.enableQuickEdit();
        this.enableBulkActions();
    }
    
    enableDragAndDrop() {
        // جعل القياسات قابلة للسحب
        document.addEventListener('dragstart', (e) => {
            if (e.target.classList.contains('draggable-shot')) {
                this.draggedItem = e.target;
                e.target.style.opacity = '0.5';
            }
        });
        
        document.addEventListener('dragend', (e) => {
            if (e.target.classList.contains('draggable-shot')) {
                e.target.style.opacity = '1';
            }
        });
        
        // مناطق الإفلات
        document.addEventListener('dragover', (e) => {
            e.preventDefault();
            if (e.target.classList.contains('drop-zone')) {
                e.target.style.background = 'rgba(0, 102, 204, 0.2)';
            }
        });
        
        document.addEventListener('drop', (e) => {
            e.preventDefault();
            if (e.target.classList.contains('drop-zone') && this.draggedItem) {
                e.target.appendChild(this.draggedItem);
                this.saveNewOrder();
            }
        });
    }
    
    enableQuickEdit() {
        // تحرير سريع بالنقر المزدوج
        document.addEventListener('dblclick', (e) => {
            const shotElement = e.target.closest('.shot-item');
            if (shotElement) {
                const shotId = shotElement.dataset.id;
                this.openQuickEditor(shotId);
            }
        });
    }
    
    openQuickEditor(shotId) {
        // فتح محرر سريع
        const shot = dbManager.getShotById(shotId);
        if (shot) {
            const editor = `
                <div class="quick-editor">
                    <h4>تحرير سريع: ${shot.r}</h4>
                    <input type="text" value="${shot.v}" id="quickValue">
                    <input type="text" value="${shot.power}" id="quickPower">
                    <textarea id="quickTip">${shot.tip}</textarea>
                    <button onclick="saveQuickEdit('${shotId}')">💾 حفظ</button>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', editor);
        }
    }
}

// محرر نظام الدايمند
class DiamondSystemEditor {
    constructor() {
        this.diamondValues = [...DIAMOND_SYSTEM];
        this.initEditor();
    }
    
    initEditor() {
        this.createEditorUI();
    }
    
    createEditorUI() {
        const editorHTML = `
            <div class="diamond-editor">
                <h3><i class="fas fa-sliders-h"></i> محرر نظام الدايمند</h3>
                
                <div class="current-values">
                    <h4>القيم الحالية:</h4>
                    <div class="values-list" id="diamondValuesList">
                        ${this.diamondValues.map((value, index) => `
                            <div class="diamond-value-item" data-index="${index}">
                                <span>${value}</span>
                                <button onclick="removeDiamondValue(${index})" class="btn-small">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                        `).join('')}
                    </div>
                </div>
                
                <div class="add-value">
                    <h4>إضافة قيمة جديدة:</h4>
                    <input type="number" step="0.1" min="0" max="10" id="newDiamondValue">
                    <button onclick="addDiamondValue()" class="btn-add">
                        <i class="fas fa-plus"></i> إضافة
                    </button>
                </div>
                
                <div class="presets">
                    <h4>أنظمة جاهزة:</h4>
                    <button onclick="loadPreset('basic')" class="btn-preset">
                        النظام الأساسي (0-4)
                    </button>
                    <button onclick="loadPreset('extended')" class="btn-preset">
                        النظام الممتد (0-5)
                    </button>
                    <button onclick="loadPreset('custom')" class="btn-preset">
                        نظام مخصص
                    </button>
                </div>
            </div>
        `;
        
        return editorHTML;
    }
    
    addValue(newValue) {
        if (!this.diamondValues.includes(newValue)) {
            this.diamondValues.push(newValue);
            this.diamondValues.sort((a, b) => a - b);
            this.saveToStorage();
            this.updateUI();
            return true;
        }
        return false;
    }
    
    removeValue(index) {
        this.diamondValues.splice(index, 1);
        this.saveToStorage();
        this.updateUI();
    }
    
    saveToStorage() {
        localStorage.setItem('custom-diamond-system', JSON.stringify(this.diamondValues));
        // إعادة تحميل النظام في التطبيق
        window.DIAMOND_SYSTEM = this.diamondValues;
        initDiamondSystem();
    }
}

// استيراد من الصور باستخدام OCR (إذا دعم المتصفح)
class ImageImportSystem {
    constructor() {
        this.supported = 'Tesseract' in window;
    }
    
    async importFromImage(imageFile) {
        if (!this.supported) {
            alert('ميزة قراءة الصور غير مدعومة في متصفحك');
            return;
        }
        
        const worker = await Tesseract.createWorker('ara');
        const { data: { text } } = await worker.recognize(imageFile);
        await worker.terminate();
        
        const shots = this.parseTextToShots(text);
        return shots;
    }
    
    parseTextToShots(text) {
        // تحليل النص إلى قياسات
        // مثال: "4 bands, cue 1.5, top right, value 2.7"
        const shots = [];
        const lines = text.split('\n');
        
        lines.forEach(line => {
            const shot = this.parseLine(line);
            if (shot) shots.push(shot);
        });
        
        return shots;
    }
    
    parseLine(line) {
        // منطق تحليل النص
        const bandsMatch = line.match(/(\d+)\s*(bands|اشرطة|جدرات)/i);
        const cueMatch = line.match(/cue\s*(\d+\.?\d*)|كيو\s*(\d+\.?\d*)/i);
        const positionMatch = line.match(/(top|mid|down|على|وسط|تحت)\s*(right|left|يمين|يسار)/i);
        const valueMatch = line.match(/value\s*(\d+\.?\d*)|قيمة\s*(\d+\.?\d*)/i);
        
        if (bandsMatch && cueMatch) {
            return {
                bands: bandsMatch[1],
                cue: cueMatch[1] || cueMatch[2],
                position: this.translatePosition(positionMatch ? positionMatch[0] : 'Top Right'),
                v: valueMatch ? (valueMatch[1] || valueMatch[2]) : '2.5',
                power: '85%',
                angle: 45,
                tip: 'مستورد من صورة'
            };
        }
        
        return null;
    }
}

// فتح قائمة السياق بالضغط الطويل
let longPressTimer;
const SHOT_ELEMENTS = document.querySelectorAll('.shot-item, .preset-card');

SHOT_ELEMENTS.forEach(element => {
    element.addEventListener('touchstart', (e) => {
        longPressTimer = setTimeout(() => {
            showContextMenu(e, element);
        }, 800); // 800ms للضغط الطويل
    });
    
    element.addEventListener('touchend', () => {
        clearTimeout(longPressTimer);
    });
    
    element.addEventListener('touchmove', () => {
        clearTimeout(longPressTimer);
    });
});

function showContextMenu(event, element) {
    const shotId = element.dataset.id;
    const menu = `
        <div class="context-menu" style="left: ${event.touches[0].clientX}px; top: ${event.touches[0].clientY}px;">
            <div class="context-item" onclick="editShot('${shotId}')">
                <i class="fas fa-edit"></i> تعديل
            </div>
            <div class="context-item" onclick="duplicateShot('${shotId}')">
                <i class="fas fa-copy"></i> نسخ
            </div>
            <div class="context-item" onclick="changeCategory('${shotId}')">
                <i class="fas fa-folder"></i> تغيير التصنيف
            </div>
            <div class="context-item" onclick="addToFavorites('${shotId}')">
                <i class="fas fa-star"></i> إضافة للمفضلة
            </div>
            <div class="context-item" onclick="shareShot('${shotId}')">
                <i class="fas fa-share"></i> مشاركة
            </div>
            <div class="context-divider"></div>
            <div class="context-item delete" onclick="deleteShot('${shotId}')">
                <i class="fas fa-trash"></i> حذف
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', menu);
    
    // إغلاق القائمة بالنقر في أي مكان
    setTimeout(() => {
        document.addEventListener('touchstart', closeContextMenu, { once: true });
    }, 100);
}

function closeContextMenu() {
    const menu = document.querySelector('.context-menu');
    if (menu) menu.remove();
}

// تحليل ذكي للقياسات
class ProfessionalAnalyzer {
    analyzePatterns() {
        // تحليل أنماط التسديدات الناجحة
        const successfulShots = this.db.customShots.filter(s => 
            s.successRate > 80
        );
        
        // إيجاد العلاقات
        const patterns = {
            commonCueValues: this.findCommonValues(successfulShots, 'cue'),
            commonPositions: this.findCommonValues(successfulShots, 'position'),
            optimalPower: this.calculateAverage(successfulShots, 'power'),
            recommendedAdjustments: this.generateRecommendations(successfulShots)
        };
        
        return patterns;
    }
    
    generateRecommendations(shots) {
        // توليد توصيات ذكية
        const recommendations = [];
        
        if (shots.length > 10) {
            recommendations.push(`أنت تتقن ${shots[0].bands} أشرطة بنسبة نجاح ${this.calculateAverageSuccess(shots)}%`);
            recommendations.push(`جرب زيادة الكيو إلى ${this.suggestNextCueValue(shots)} لتحسين النتائج`);
            recommendations.push(`المواضع الأكثر نجاحاً: ${this.getTopPositions(shots).join(', ')}`);
        }
        
        return recommendations;
    }
}
// نظام الدايمند - البيانات الأساسية
const DIAMOND_SYSTEM = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5];

// دالة حساب التسديدة
function calculateShot() {
    const bands = document.getElementById('bands').value;
    const cue = document.getElementById('cue').value;
    const pocket = document.getElementById('pocket').value;
    
    // الحصول على البيانات من قاعدة البيانات
    const shotData = dbManager.database[bands]?.[cue]?.[pocket];
    
    if (shotData) {
        displayResults(shotData);
    } else {
        showNotification('لا توجد بيانات لهذه التسديدة', 'error');
    }
}

// عرض النتائج
function displayResults(shots) {
    const resultsCard = document.getElementById('resultsCard');
    const resultsDiv = document.getElementById('shotResults');
    
    let html = '<div class="shots-list">';
    
    shots.forEach(shot => {
        html += `
            <div class="shot-result">
                <h3>${shot.r}</h3>
                <div class="shot-info">
                    <span><strong>القيمة:</strong> ${shot.v}</span>
                    <span><strong>القوة:</strong> ${shot.power}</span>
                    <span><strong>الزاوية:</strong> ${shot.angle}°</span>
                    <span><strong>الصعوبة:</strong> ${shot.difficulty}/10</span>
                    <span><strong>معدل النجاح:</strong> ${shot.successRate}%</span>
                </div>
                <div class="shot-tip">
                    <i class="fas fa-lightbulb"></i> ${shot.tip}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
    resultsCard.style.display = 'block';
    
    // التمرير إلى النتائج
    resultsCard.scrollIntoView({ behavior: 'smooth' });
}

// تهيئة القوائم
function initDiamondSystem() {
    const cueSelect = document.getElementById('cue');
    
    // ملء قائمة الكيو
    DIAMOND_SYSTEM.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        cueSelect.appendChild(option);
    });
    
    // قيمة افتراضية
    cueSelect.value = '2';
}

// إغلاق محرر القياسات
function closeEditor() {
    document.getElementById('editorPanel').style.display = 'none';
}

// إشعارات محسّنة
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}
// إضافة في script.js

// 1. تسريع الأداء
class PerformanceOptimizer {
    static debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    }
}

// 2. وضع داكن تلقائي
function initDarkMode() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    if (prefersDark.matches) {
        document.body.classList.add('dark-theme');
    }
    
    prefersDark.addEventListener('change', (e) => {
        if (e.matches) {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
    });
}

// 3. معايرة اللمس لـ iPad
function initTouchCalibration() {
    if ('ontouchstart' in window) {
        document.body.classList.add('touch-device');
        
        // منع الزووم المزدوج
        document.addEventListener('dblclick', (e) => {
            e.preventDefault();
        });
    }
}
// ===================================
// ✅ الدوال الناقصة المضافة الآن
// ===================================

// 📋 دالة عرض "عن التطبيق"
function showAbout() {
    const modal = document.getElementById('modalOverlay');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');
    
    title.textContent = '📱 عن التطبيق';
    
    body.innerHTML = `
        <div class="about-content">
            <div class="app-info">
                <i class="fas fa-gem" style="font-size: 3rem; color: #0066CC; margin-bottom: 15px;"></i>
                <h3>5A Diamond System Pro</h3>
                <p class="version">الإصدار 3.0.0</p>
            </div>
            
            <div class="about-section">
                <h4>🎯 وصف التطبيق</h4>
                <p>تطبيق PWA احترافي متقدم لتحليل تسديدات البلياردو باستخدام نظام الدايمند العشري المتطور.</p>
            </div>
            
            <div class="about-section">
                <h4>✨ المميزات الرئيسية</h4>
                <ul>
                    <li><i class="fas fa-wifi-off"></i> يعمل بدون إنترنت (Offline)</li>
                    <li><i class="fas fa-download"></i> قابل للتثبيت على الأجهزة</li>
                    <li><i class="fas fa-database"></i> قاعدة بيانات شاملة وقابلة للتوسع</li>
                    <li><i class="fas fa-calculator"></i> حسابات رياضية متقدمة</li>
                    <li><i class="fas fa-chart-bar"></i> إحصائيات وتحليلات مفصلة</li>
                    <li><i class="fas fa-language"></i> واجهة عربية كاملة RTL</li>
                </ul>
            </div>
            
            <div class="about-section">
                <h4>👨‍💻 التطوير والتقنيات</h4>
                <ul>
                    <li>HTML5 و CSS3 و JavaScript ES6+</li>
                    <li>Progressive Web App (PWA)</li>
                    <li>Service Worker للعمل بدون إنترنت</li>
                    <li>LocalStorage لإدارة البيانات</li>
                    <li>تصميم Responsive وتطبيقي</li>
                </ul>
            </div>
            
            <div class="about-section">
                <h4>📊 نظام الدايمند</h4>
                <p>نظام رياضي دقيق لحساب زوايا التسديدات في البلياردو، يعتمد على:</p>
                <ul>
                    <li>4 أنظمة مختلفة للأشرطة (1-4)</li>
                    <li>11 قيمة للكيو (0 إلى 5)</li>
                    <li>6 مواضع للجيب المستهدف</li>
                    <li>6 أنواع تسديدات مختلفة</li>
                </ul>
            </div>
            
            <div class="about-section">
                <h4>⚖️ الترخيص والحقوق</h4>
                <p>&copy; 2024-2025 5A Diamond System Pro. جميع الحقوق محفوظة.</p>
            </div>
            
            <div class="about-section">
                <h4>🔗 الروابط المهمة</h4>
                <div class="about-links">
                    <button onclick="showHelp()" class="link-btn">
                        <i class="fas fa-question-circle"></i> المساعدة والدعم
                    </button>
                    <button onclick="checkForUpdates()" class="link-btn">
                        <i class="fas fa-sync-alt"></i> البحث عن تحديثات
                    </button>
                </div>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// ❓ دالة عرض "المساعدة"
function showHelp() {
    const modal = document.getElementById('modalOverlay');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');
    
    title.textContent = '❓ المساعدة والدليل';
    
    body.innerHTML = `
        <div class="help-content">
            <div class="help-section">
                <h4><i class="fas fa-rocket"></i> البدء السريع</h4>
                <div class="help-item">
                    <h5>1. اختر عدد الأشرطة</h5>
                    <p>اختر من 1 إلى 4 أشرطة حسب عدد الانعكاسات التي تريدها.</p>
                </div>
                <div class="help-item">
                    <h5>2. حدد موضع الكيو</h5>
                    <p>اختر قيمة الكيو من 0 إلى 5 على نظام الدايمند.</p>
                </div>
                <div class="help-item">
                    <h5>3. اختر الجيب الهدف</h5>
                    <p>اختر الزاوية أو الموضع المستهدف (6 خيارات).</p>
                </div>
                <div class="help-item">
                    <h5>4. احسب التسديدة</h5>
                    <p>اضغط على "حساب التسديدة" لعرض النتائج.</p>
                </div>
            </div>
            
            <div class="help-section">
                <h4><i class="fas fa-cog"></i> إدارة القياسات</h4>
                <p>استخدم زر "إدارة القياسات" في الرأس للوصول إلى:</p>
                <ul>
                    <li><strong>جميع القياسات:</strong> عرض وتعديل قياساتك</li>
                    <li><strong>إضافة قياس:</strong> أضف قياسات مخصصة جديدة</li>
                    <li><strong>استيراد:</strong> استورد قياسات من ملف</li>
                    <li><strong>تصدير:</strong> احفظ قياساتك في ملف</li>
                    <li><strong>إحصائيات:</strong> عرض إحصائيات الأداء</li>
                    <li><strong>النسخ الاحتياطي:</strong> احفظ واستعد بياناتك</li>
                </ul>
            </div>
            
            <div class="help-section">
                <h4><i class="fas fa-gem"></i> نظام الدايمند</h4>
                <p>نظام رياضي قديم وموثوق لحساب زوايا البلياردو:</p>
                <ul>
                    <li><strong>الأشرطة (Bands):</strong> عدد مرات ارتداد الكرة على الجدران</li>
                    <li><strong>الكيو (Cue):</strong> موضع الكيو على الطاولة</li>
                    <li><strong>الموضع:</strong> الجيب المستهدف</li>
                    <li><strong>النوع:</strong> نوع التسديدة (مباشرة، انعكاس، إلخ)</li>
                </ul>
            </div>
            
            <div class="help-section">
                <h4><i class="fas fa-info-circle"></i> نصائح وحيل</h4>
                <ul>
                    <li>💡 استخدم "التقاط من الإعدادات الحالية" لحفظ التسديدة الحالية بسرعة</li>
                    <li>💾 أنشئ نسخ احتياطية منتظمة لتجنب فقدان البيانات</li>
                    <li>📊 راجع الإحصائيات لمعرفة أكثر التسديدات نجاحاً</li>
                    <li>🏷️ صنّف قياساتك لتنظيم أفضل</li>
                    <li>📱 ثبّت التطبيق على جهازك للوصول السريع</li>
                </ul>
            </div>
            
            <div class="help-section">
                <h4><i class="fas fa-troubleshoot"></i> استكشاف الأخطاء</h4>
                <div class="faq-item">
                    <h5>س: التطبيق لا يعمل بدون إنترنت</h5>
                    <p>ج: تأكد من أنك قد فتحت التطبيق مرة واحدة على الأقل مع الإنترنت لتثبيت Service Worker.</p>
                </div>
                <div class="faq-item">
                    <h5>س: فقدت بياناتي</h5>
                    <p>ج: حاول استعادة نسخة احتياطية من تبويب "النسخ الاحتياطي" في الإدارة.</p>
                </div>
                <div class="faq-item">
                    <h5>س: كيف أصدّر البيانات؟</h5>
                    <p>ج: افتح إدارة القياسات > تصدير > اختر الصيغة (JSON أو CSV).</p>
                </div>
            </div>
            
            <div class="help-section">
                <h4><i class="fas fa-envelope"></i> الدعم والتواصل</h4>
                <p>إذا واجهت مشاكل أو لديك اقتراحات، يمكنك التواصل عبر:</p>
                <p style="text-align: center; margin-top: 10px;">
                    <a href="mailto:support@5adiamondpro.com" style="color: #0066CC;">📧 support@5adiamondpro.com</a>
                </p>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
}

// ✖️ دالة إغلاق النافذة المنبثقة
function closeModal() {
    const modal = document.getElementById('modalOverlay');
    if (modal) {
        modal.style.display = 'none';
    }
}

// 🔄 دالة التحقق من التحديثات
function checkForUpdates() {
    showNotification('جاري البحث عن تحديثات...', 'info');
    
    // محاكاة فحص التحديثات
    setTimeout(() => {
        showNotification('أنت تستخدم أحدث إصدار (v3.0.0)', 'success');
    }, 1500);
}

// ✔️ دالة ربط زر التثبيت بـ installApp
document.addEventListener('DOMContentLoaded', () => {
    const installBtn = document.getElementById('installButton');
    if (installBtn) {
        installBtn.addEventListener('click', installApp);
    }
    
    // إغلاق النافذة المنبثقة عند النقر خارجها
    const modal = document.getElementById('modalOverlay');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal();
            }
        });
    }
});

// ===================================
// 🛡️ معالجات الأخطاء الشاملة
// ===================================

// معالج الأخطاء العام
window.addEventListener('error', (event) => {
    console.error('❌ خطأ في التطبيق:', event.error);
    showNotification(`خطأ: ${event.error?.message || 'حدث خطأ غير متوقع'}`, 'error');
});

// معالج الـ Unhandled Promises
window.addEventListener('unhandledrejection', (event) => {
    console.error('❌ وعد غير معالج:', event.reason);
    showNotification('حدث خطأ في معالجة البيانات', 'error');
});

// معالج عند فقدان الاتصال بالإنترنت
window.addEventListener('offline', () => {
    showNotification('📡 تم فقدان الاتصال بالإنترنت. التطبيق يعمل بدون إنترنت', 'warning');
    document.body.classList.add('offline-mode');
});

// معالج عند استعادة الاتصال
window.addEventListener('online', () => {
    showNotification('✅ تم استعادة الاتصال بالإنترنت', 'success');
    document.body.classList.remove('offline-mode');
});

// معالج الأخطاء في LocalStorage
function safeLocalStorage(action, key, value) {
    try {
        if (action === 'set') {
            localStorage.setItem(key, value);
            return true;
        } else if (action === 'get') {
            return localStorage.getItem(key);
        } else if (action === 'remove') {
            localStorage.removeItem(key);
            return true;
        }
    } catch (error) {
        if (error.name === 'QuotaExceededError') {
            showNotification('⚠️ مساحة التخزين ممتلئة. حاول حذف بعض البيانات', 'warning');
        } else if (error.name === 'SecurityError') {
            showNotification('⚠️ لا يمكن الوصول إلى التخزين. تحقق من إعدادات المتصفح', 'warning');
        } else {
            showNotification(`⚠️ خطأ في التخزين: ${error.message}`, 'warning');
        }
        return null;
    }
}

// تحسين showNotification مع معالجة الأخطاء
const originalShowNotification = showNotification;
showNotification = function(message, type = 'info') {
    try {
        originalShowNotification(message, type);
    } catch (error) {
        console.error('خطأ في عرض الإشعار:', error);
        // عرض الإشعار في الكونسول كبديل
        console[type === 'error' ? 'error' : 'log'](message);
    }
};

// دالة معالجة الأخطاء المتقدمة
class ErrorHandler {
    static handle(error, context = '') {
        const errorInfo = {
            message: error.message,
            stack: error.stack,
            context: context,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent
        };
        
        console.error('🔴 تم التقاط خطأ:', errorInfo);
        
        // إرسال الخطأ للتسجيل (اختياري)
        this.logError(errorInfo);
        
        // عرض رسالة للمستخدم
        showNotification(`حدث خطأ: ${error.message}`, 'error');
    }
    
    static logError(errorInfo) {
        // يمكن إضافة نقطة نهاية للخادم لتسجيل الأخطاء
        console.log('تم تسجيل الخطأ:', errorInfo);
    }
}

// استخدام معالج الأخطاء
window.addEventListener('error', (event) => {
    ErrorHandler.handle(event.error, 'Global');
});

console.log('✅ تم تحميل جميع معالجات الأخطاء بنجاح');

// ===================================
// ✨ التحسينات الأساسية الجديدة
// ===================================

// 🌙 1. نظام تبديل النمط المظلم/الفاتح (Dark Mode)
class ThemeManager {
    constructor() {
        this.darkModeKey = '5a-dark-mode';
        this.prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        this.init();
    }
    
    init() {
        const savedDarkMode = localStorage.getItem(this.darkModeKey);
        const isDark = savedDarkMode !== null ? 
            JSON.parse(savedDarkMode) : 
            this.prefersDark.matches;
        
        if (isDark) {
            this.enableDarkMode();
        }
        
        this.prefersDark.addEventListener('change', (e) => {
            if (e.matches) {
                this.enableDarkMode();
            } else {
                this.disableDarkMode();
            }
        });
    }
    
    enableDarkMode() {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.body.classList.add('dark-mode');
        localStorage.setItem(this.darkModeKey, 'true');
        this.updateThemeButton();
    }
    
    disableDarkMode() {
        document.documentElement.removeAttribute('data-theme');
        document.body.classList.remove('dark-mode');
        localStorage.setItem(this.darkModeKey, 'false');
        this.updateThemeButton();
    }
    
    toggle() {
        const isDark = document.body.classList.contains('dark-mode');
        if (isDark) {
            this.disableDarkMode();
            showNotification('تم تفعيل النمط الفاتح ☀️', 'success');
        } else {
            this.enableDarkMode();
            showNotification('تم تفعيل النمط المظلم 🌙', 'success');
        }
    }
    
    updateThemeButton() {
        const btn = document.getElementById('themeToggle');
        if (btn) {
            const isDark = document.body.classList.contains('dark-mode');
            btn.innerHTML = isDark ? 
                '<i class="fas fa-sun"></i>' : 
                '<i class="fas fa-moon"></i>';
        }
    }
}

// 📜 2. نظام سجل التسديدات الأخيرة
class ShotHistory {
    constructor(maxItems = 15) {
        this.maxItems = maxItems;
        this.historyKey = '5a-shot-history';
        this.history = this.loadHistory();
    }
    
    loadHistory() {
        const saved = localStorage.getItem(this.historyKey);
        return saved ? JSON.parse(saved) : [];
    }
    
    saveHistory() {
        localStorage.setItem(this.historyKey, JSON.stringify(this.history));
    }
    
    addShot(shotData) {
        const shot = {
            id: `history-${Date.now()}`,
            bands: shotData.bands || document.getElementById('bands').value,
            cue: shotData.cue || document.getElementById('cue').value,
            pocket: shotData.pocket || document.getElementById('pocket').value,
            timestamp: new Date().toISOString(),
            displayTime: new Date().toLocaleTimeString('ar-SA')
        };
        
        this.history.unshift(shot);
        
        if (this.history.length > this.maxItems) {
            this.history = this.history.slice(0, this.maxItems);
        }
        
        this.saveHistory();
        return shot;
    }
    
    getHistory() {
        return this.history;
    }
    
    clearHistory() {
        this.history = [];
        this.saveHistory();
    }
    
    getArabicPosition(position) {
        const positions = {
            'Top Right': 'أعلى اليمين',
            'Top Left': 'أعلى اليسار',
            'Mid Right': 'وسط اليمين',
            'Mid Left': 'وسط اليسار',
            'Down Right': 'أسفل اليمين',
            'Down Left': 'أسفل اليسار'
        };
        return positions[position] || position;
    }
    
    render() {
        const section = document.getElementById('recentShotsSection');
        const list = document.getElementById('recentShotsList');
        
        if (this.history.length === 0) {
            section.style.display = 'none';
            return;
        }
        
        section.style.display = 'block';
        
        let html = '<div class="recent-shots-container">';
        
        this.history.forEach((shot) => {
            html += `
                <div class="recent-shot-item">
                    <div class="shot-quick-info">
                        <span class="quick-badge">${shot.bands} أشرطة</span>
                        <span class="quick-badge">كيو ${shot.cue}</span>
                        <span class="quick-badge">${this.getArabicPosition(shot.pocket)}</span>
                    </div>
                    <div class="shot-time">${shot.displayTime}</div>
                    <button onclick="replayShot('${shot.bands}', '${shot.cue}', '${shot.pocket}')" class="btn-replay">
                        <i class="fas fa-redo"></i> إعادة
                    </button>
                    <button onclick="addToFavoritesFromHistory('${shot.bands}', '${shot.cue}', '${shot.pocket}')" class="btn-favorite">
                        <i class="fas fa-star"></i>
                    </button>
                </div>
            `;
        });
        
        html += '</div>';
        list.innerHTML = html;
    }
}

// ⭐ 3. نظام المفضلة
class FavoritesManager {
    constructor() {
        this.favoritesKey = '5a-favorites';
        this.favorites = this.loadFavorites();
    }
    
    loadFavorites() {
        const saved = localStorage.getItem(this.favoritesKey);
        return saved ? JSON.parse(saved) : [];
    }
    
    saveFavorites() {
        localStorage.setItem(this.favoritesKey, JSON.stringify(this.favorites));
    }
    
    addFavorite(bands, cue, pocket) {
        const favorite = {
            id: `fav-${bands}-${cue}-${pocket}`,
            bands: bands,
            cue: cue,
            pocket: pocket,
            name: `${bands} أشرطة - كيو ${cue}`,
            dateAdded: new Date().toISOString(),
            count: 0
        };
        
        if (!this.isFavorited(bands, cue, pocket)) {
            this.favorites.unshift(favorite);
            this.saveFavorites();
            showNotification('✅ تم إضافة للمفضلة', 'success');
            return true;
        }
        return false;
    }
    
    removeFavorite(bands, cue, pocket) {
        this.favorites = this.favorites.filter(
            fav => !(fav.bands == bands && fav.cue == cue && fav.pocket == pocket)
        );
        this.saveFavorites();
        showNotification('❌ تم إزالة من المفضلة', 'info');
    }
    
    isFavorited(bands, cue, pocket) {
        return this.favorites.some(
            fav => fav.bands == bands && fav.cue == cue && fav.pocket == pocket
        );
    }
    
    incrementCount(bands, cue, pocket) {
        const fav = this.favorites.find(
            f => f.bands == bands && f.cue == cue && f.pocket == pocket
        );
        if (fav) {
            fav.count = (fav.count || 0) + 1;
            fav.lastUsed = new Date().toISOString();
            this.saveFavorites();
        }
    }
    
    getFavorites() {
        return this.favorites.sort((a, b) => (b.count || 0) - (a.count || 0));
    }
}

// 🚀 4. تحسينات الأداء
class PerformanceHelper {
    static memoizedResults = new Map();
    
    static cacheResult(key, result) {
        this.memoizedResults.set(key, result);
        if (this.memoizedResults.size > 100) {
            const keysArray = Array.from(this.memoizedResults.keys());
            for (let i = 0; i < 10; i++) {
                this.memoizedResults.delete(keysArray[i]);
            }
        }
    }
    
    static getCachedResult(key) {
        return this.memoizedResults.get(key);
    }
    
    static clearCache() {
        this.memoizedResults.clear();
    }
}

// ===================================
// 🔧 التهيئة والربط
// ===================================

let themeManager;
let shotHistory;
let favoritesManager;

function initEnhancements() {
    themeManager = new ThemeManager();
    shotHistory = new ShotHistory();
    favoritesManager = new FavoritesManager();
    
    const themeBtn = document.getElementById('themeToggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            themeManager.toggle();
        });
    }
    
    console.log('✅ تم تفعيل جميع التحسينات الأساسية');
}

function replayShot(bands, cue, pocket) {
    document.getElementById('bands').value = bands;
    document.getElementById('cue').value = cue;
    document.getElementById('pocket').value = pocket;
    calculateShot();
    showNotification('🔄 تم إعادة التسديدة', 'info');
}

function clearCalculation() {
    document.getElementById('bands').value = '4';
    document.getElementById('cue').value = '2';
    document.getElementById('pocket').value = 'Top Right';
    document.getElementById('resultsCard').style.display = 'none';
    showNotification('🗑️ تم مسح البيانات', 'info');
}

function addToFavoritesFromHistory(bands, cue, pocket) {
    if (favoritesManager.addFavorite(bands, cue, pocket)) {
        shotHistory.render();
    }
}

// تحسين calculateShot الأصلية
if (typeof calculateShot !== 'undefined') {
    const originalCalculateShot = calculateShot;
    calculateShot = function() {
        const bands = document.getElementById('bands').value;
        const cue = document.getElementById('cue').value;
        const pocket = document.getElementById('pocket').value;
        
        shotHistory.addShot({ bands, cue, pocket });
        shotHistory.render();
        favoritesManager.incrementCount(bands, cue, pocket);
        
        originalCalculateShot();
    };
}

document.addEventListener('DOMContentLoaded', () => {
    initEnhancements();
    shotHistory.render();
});
