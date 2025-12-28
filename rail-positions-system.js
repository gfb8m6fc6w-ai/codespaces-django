// 📁 rail-positions-system.js
// نظام شامل لمواقع الجدران والكرة البيضاء والهدف

/**
 * فئة لإدارة مواقع الجدران والكرات
 */
class RailPositionsSystem {
    constructor() {
        // الجانب الطويل (0-8 قدم)
        this.longRailPositions = [
            8.0, 7.5, 7.1, 7.0, 6.9, 6.75, 6.6, 6.5, 6.4, 6.25,
            6.1, 6.0, 5.9, 5.75, 5.6, 5.5, 5.4, 5.25, 5.1, 5.0,
            4.9, 4.5, 4.3, 4.0, 3.6, 3.5, 3.4, 3.1, 3.0, 2.9,
            2.75, 2.6, 2.5, 2.4, 2.25, 2.1, 2.0, 1.9, 1.75, 1.6,
            1.5, 1.4, 1.25, 1.1, 1.0, 0.9, 0.75, 0.5, 0.25, 0.0
        ];

        // الجانب القصير (0-4 قدم)
        this.shortRailPositions = [
            0.0, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 1.0, 1.1, 1.25,
            1.4, 1.5, 1.6, 1.75, 1.9, 2.0, 2.1, 2.25, 2.4, 2.5,
            2.6, 2.75, 2.9, 3.0, 3.1, 3.25, 3.5, 3.75, 4.0
        ];

        // مواقع الكرة البيضاء على الجانب الطويل
        this.whiteBallLongRailPositions = [
            1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5,
            6.0, 6.5, 7.0, 7.5
        ];

        // مواقع الكرة البيضاء على الجانب القصير
        this.whiteBallShortRailPositions = [
            0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5
        ];

        // مواقع الهدف على الجانب الطويل
        this.targetLongRailPositions = [
            0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
            5.5, 6.0, 6.5, 7.0, 7.5, 8.0
        ];

        // مواقع الهدف على الجانب القصير
        this.targetShortRailPositions = [
            0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5,
            2.75, 3.0, 3.25, 3.5, 3.75, 4.0
        ];
    }

    /**
     * الحصول على جميع مواقع الكرة البيضاء المتاحة
     */
    getAllWhiteBallPositions(rail = 'long') {
        return rail === 'long' ? this.whiteBallLongRailPositions : this.whiteBallShortRailPositions;
    }

    /**
     * الحصول على جميع مواقع الهدف المتاحة
     */
    getAllTargetPositions(rail = 'long') {
        return rail === 'long' ? this.targetLongRailPositions : this.targetShortRailPositions;
    }

    /**
     * التحقق من أن الموقع صحيح
     */
    isValidPosition(position, positionType = 'long') {
        if (positionType === 'long') {
            return this.longRailPositions.includes(position);
        } else {
            return this.shortRailPositions.includes(position);
        }
    }

    /**
     * الحصول على أقرب موقع متاح
     */
    getNearestPosition(position, rail = 'long') {
        const positions = rail === 'long' ? this.longRailPositions : this.shortRailPositions;
        return positions.reduce((nearest, pos) => {
            return Math.abs(pos - position) < Math.abs(nearest - position) ? pos : nearest;
        });
    }

    /**
     * الحصول على جميع المواقع في نطاق محدد
     */
    getPositionsInRange(min, max, rail = 'long') {
        const positions = rail === 'long' ? this.longRailPositions : this.shortRailPositions;
        return positions.filter(pos => pos >= min && pos <= max);
    }

    /**
     * تحويل قياس القدم إلى نسبة مئوية
     */
    positionToPercentage(position, rail = 'long') {
        const maxPosition = rail === 'long' ? 8.0 : 4.0;
        return (position / maxPosition) * 100;
    }

    /**
     * تحويل نسبة مئوية إلى قياس القدم
     */
    percentageToPosition(percentage, rail = 'long') {
        const maxPosition = rail === 'long' ? 8.0 : 4.0;
        return (percentage / 100) * maxPosition;
    }
}

/**
 * فئة لإدارة بيانات اللقطة (Shot Data)
 */
class ShotDataManager {
    constructor() {
        this.railsSystem = new RailPositionsSystem();
        this.shots = [];
        this.currentShot = null;
    }

    /**
     * إنشاء لقطة جديدة
     */
    createShot(config = {}) {
        const shot = {
            id: Date.now(),
            rails: config.rails || 3,
            whiteBallMeasurement: config.whiteBallMeasurement || 1.0,
            whiteBallRail: config.whiteBallRail || 'long',
            targetMeasurement: config.targetMeasurement || 4.0,
            targetRail: config.targetRail || 'long',
            cueMeasurement: config.cueMeasurement || 5.0,
            cueHeight: config.cueHeight || 'center',
            cuePower: config.cuePower || 50,
            spinType: config.spinType || 'none', // none, topspin, backspin, english
            notes: config.notes || '',
            timestamp: Date.now(),
            difficulty: this.calculateDifficulty(config),
            geometry: null
        };

        return shot;
    }

    /**
     * التحقق من صحة بيانات اللقطة
     */
    validateShot(shot) {
        const errors = [];

        // التحقق من عدد الجدران
        if (shot.rails < 1 || shot.rails > 4) {
            errors.push('عدد الجدران يجب أن يكون بين 1 و 4');
        }

        // التحقق من موقع الكرة البيضاء
        if (!this.railsSystem.isValidPosition(shot.whiteBallMeasurement, shot.whiteBallRail)) {
            const nearest = this.railsSystem.getNearestPosition(shot.whiteBallMeasurement, shot.whiteBallRail);
            console.warn(`موقع الكرة البيضاء ${shot.whiteBallMeasurement} غير صحيح، استخدام ${nearest}`);
            shot.whiteBallMeasurement = nearest;
        }

        // التحقق من موقع الهدف
        if (!this.railsSystem.isValidPosition(shot.targetMeasurement, shot.targetRail)) {
            const nearest = this.railsSystem.getNearestPosition(shot.targetMeasurement, shot.targetRail);
            console.warn(`موقع الهدف ${shot.targetMeasurement} غير صحيح، استخدام ${nearest}`);
            shot.targetMeasurement = nearest;
        }

        // التحقق من قياس العصا
        if (shot.cueMeasurement < 0 || shot.cueMeasurement > 20) {
            errors.push('قياس العصا يجب أن يكون بين 0 و 20');
        }

        return { isValid: errors.length === 0, errors };
    }

    /**
     * حساب درجة صعوبة اللقطة
     */
    calculateDifficulty(config) {
        let difficulty = 0;

        // كلما زاد عدد الجدران، زادت الصعوبة
        difficulty += config.rails * 25;

        // المسافة بين الكرة البيضاء والهدف
        const whiteBallPos = config.whiteBallMeasurement || 1.0;
        const targetPos = config.targetMeasurement || 4.0;
        const distance = Math.abs(whiteBallPos - targetPos);
        difficulty += Math.min(distance * 10, 25);

        // قوة العصا
        const power = config.cuePower || 50;
        if (power > 70) {
            difficulty += 15; // قوة عالية أصعب
        }

        return Math.min(difficulty, 100);
    }

    /**
     * حفظ اللقطة
     */
    saveShot(shot) {
        const validation = this.validateShot(shot);
        if (!validation.isValid) {
            return { success: false, errors: validation.errors };
        }

        this.shots.push(shot);
        this.currentShot = shot;

        // حفظ في localStorage
        this.saveToLocalStorage();

        return { success: true, shot };
    }

    /**
     * الحصول على جميع اللقطات المحفوظة
     */
    getAllShots() {
        return this.shots;
    }

    /**
     * تصفية اللقطات حسب عدد الجدران
     */
    getShotsByRails(rails) {
        return this.shots.filter(shot => shot.rails === rails);
    }

    /**
     * حذف لقطة
     */
    deleteShot(shotId) {
        this.shots = this.shots.filter(shot => shot.id !== shotId);
        this.saveToLocalStorage();
    }

    /**
     * حفظ في localStorage
     */
    saveToLocalStorage() {
        try {
            localStorage.setItem('billiardsShots', JSON.stringify(this.shots));
        } catch (e) {
            console.warn('خطأ في حفظ البيانات:', e);
        }
    }

    /**
     * استحضار من localStorage
     */
    loadFromLocalStorage() {
        try {
            const data = localStorage.getItem('billiardsShots');
            this.shots = data ? JSON.parse(data) : [];
        } catch (e) {
            console.warn('خطأ في قراءة البيانات:', e);
            this.shots = [];
        }
    }
}

/**
 * فئة لحساب مسارات اللقطات
 */
class ShotPathCalculator {
    constructor(railsSystem) {
        this.railsSystem = railsSystem;
    }

    /**
     * حساب مسار اللقطة مع جدار واحد
     */
    calculateOneRailPath(shot) {
        const whiteBall = shot.whiteBallMeasurement;
        const target = shot.targetMeasurement;
        const cue = shot.cueMeasurement;

        return {
            rail: 'single',
            contact: this.calculateRailContact(whiteBall, target, cue, 1),
            path: this.generatePathCoordinates(whiteBall, target, 1),
            difficulty: shot.difficulty
        };
    }

    /**
     * حساب مسار اللقطة مع جدارين
     */
    calculateTwoRailsPath(shot) {
        const contacts = [];
        let currentPosition = shot.whiteBallMeasurement;

        for (let i = 0; i < 2; i++) {
            const contact = this.calculateRailContact(currentPosition, shot.targetMeasurement, shot.cueMeasurement, i + 1);
            contacts.push(contact);
            currentPosition = contact.position;
        }

        return {
            rail: 'double',
            contacts,
            path: this.generatePathCoordinates(shot.whiteBallMeasurement, shot.targetMeasurement, 2),
            difficulty: shot.difficulty
        };
    }

    /**
     * حساب مسار اللقطة مع ثلاثة جدران
     */
    calculateThreeRailsPath(shot) {
        const contacts = [];
        let currentPosition = shot.whiteBallMeasurement;

        for (let i = 0; i < 3; i++) {
            const contact = this.calculateRailContact(currentPosition, shot.targetMeasurement, shot.cueMeasurement, i + 1);
            contacts.push(contact);
            currentPosition = contact.position;
        }

        return {
            rail: 'triple',
            contacts,
            path: this.generatePathCoordinates(shot.whiteBallMeasurement, shot.targetMeasurement, 3),
            difficulty: shot.difficulty
        };
    }

    /**
     * حساب مسار اللقطة مع أربعة جدران
     */
    calculateFourRailsPath(shot) {
        const contacts = [];
        let currentPosition = shot.whiteBallMeasurement;

        for (let i = 0; i < 4; i++) {
            const contact = this.calculateRailContact(currentPosition, shot.targetMeasurement, shot.cueMeasurement, i + 1);
            contacts.push(contact);
            currentPosition = contact.position;
        }

        return {
            rail: 'quadruple',
            contacts,
            path: this.generatePathCoordinates(shot.whiteBallMeasurement, shot.targetMeasurement, 4),
            difficulty: shot.difficulty
        };
    }

    /**
     * حساب نقطة الاتصال مع الجدار
     */
    calculateRailContact(whiteBallPos, targetPos, cueMeasurement, railNumber) {
        // حساب زاوية الاتصال بناءً على قياس العصا
        const angle = (cueMeasurement / 20) * 90; // من 0 إلى 90 درجة

        // حساب موقع الاتصال مع الجدار
        const contactPosition = (whiteBallPos + targetPos) / 2 + (angle / 90) * 0.5;
        const clampedPosition = Math.max(0, Math.min(8, contactPosition));

        return {
            railNumber,
            position: this.railsSystem.getNearestPosition(clampedPosition),
            angle: angle,
            speed: 100 - (railNumber * 15) // تقليل السرعة مع كل جدار
        };
    }

    /**
     * توليد إحداثيات المسار
     */
    generatePathCoordinates(startPos, endPos, numberOfRails) {
        const coordinates = [
            { x: startPos, y: 0, label: 'كرة بيضاء' }
        ];

        const stepSize = (endPos - startPos) / (numberOfRails + 1);

        for (let i = 1; i <= numberOfRails; i++) {
            coordinates.push({
                x: startPos + (stepSize * i),
                y: i * 1.5,
                label: `جدار ${i}`
            });
        }

        coordinates.push({
            x: endPos,
            y: (numberOfRails + 1) * 1.5,
            label: 'الهدف'
        });

        return coordinates;
    }
}

// الحصول على مثيل عام من النظام
const railPositionsSystem = new RailPositionsSystem();
const shotDataManager = new ShotDataManager();
const shotPathCalculator = new ShotPathCalculator(railPositionsSystem);

// تصدير للاستخدام في ملفات أخرى
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        RailPositionsSystem,
        ShotDataManager,
        ShotPathCalculator
    };
}
