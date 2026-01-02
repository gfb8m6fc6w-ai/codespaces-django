# 📚 وثائق API - نظام البلياردو المتكامل

## نظرة عامة

هذه الوثائق توضح جميع نقاط نهاية API والوظائف المتاحة في نظام البلياردو 5A Diamond System Pro.

---

## 📋 جدول المحتويات

1. [مدير التخزين](#مدير-التخزين)
2. [مدير الإشعارات](#مدير-الإشعارات)
3. [مدير التصدير والاستيراد](#مدير-التصدير-والاستيراد)
4. [نظام البلياردو المتكامل](#نظام-البلياردو-المتكامل)
5. [أمثلة الاستخدام](#أمثلة-الاستخدام)

---

## مدير التخزين

### `StorageManager`

مدير محلي للتخزين المحلي مع دعم النمذجة.

#### الطرق

##### `constructor(namespace)`
```javascript
const storage = new StorageManager('my-namespace');
```

##### `save(data)`
```javascript
storage.save({ key: 'value' })
// Returns: boolean
```

##### `load()`
```javascript
const data = storage.load()
// Returns: object | null
```

##### `delete()`
```javascript
storage.delete()
// Returns: boolean
```

##### `clear()`
```javascript
storage.clear()
// Returns: boolean
```

---

## مدير الإشعارات

### `NotificationManager`

نظام إشعارات بسيط وفعال.

#### الطرق

##### `show(message, type, duration)`
```javascript
NotificationManager.show('تم بنجاح', 'success', 3000)

// أنواع الإشعارات:
// - 'success': نجاح (أخضر)
// - 'error': خطأ (أحمر)
// - 'warning': تحذير (برتقالي)
// - 'info': معلومة (أزرق)
```

---

## مدير التصدير والاستيراد

### `ExportImportManager`

إدارة تصدير واستيراد البيانات.

#### الطرق

##### `export(data, filename)`
```javascript
ExportImportManager.export(myData, 'export.json')
// تحميل الملف تلقائياً
```

##### `import(file, onSuccess, onError)`
```javascript
ExportImportManager.import(fileInput, 
  (data) => console.log('تم الاستيراد', data),
  (error) => console.error('خطأ', error)
)
```

---

## نظام البلياردو المتكامل

### `BilliardsSystem`

النظام الرئيسي الذي يجمع جميع المكونات.

#### الخصائص

- `shots`: قائمة جميع التسديدات
- `settings`: الإعدادات الحالية
- `storage`: مدير التخزين
- `backups`: مدير النسخ الاحتياطية
- `theme`: مدير الموضوع

#### الطرق

##### إدارة التسديدات

```javascript
// إضافة تسديدة
billiardSystem.addShot({
  rails: 2,
  whiteBall: 5.0,
  target: 3.0,
  angle: 45,
  power: 70,
  distance: 100,
  difficulty: 2
})

// الحصول على تسديدة
billiardSystem.getShot(shotId)

// تحديث تسديدة
billiardSystem.updateShot(shotId, { success: true })

// حذف تسديدة
billiardSystem.deleteShot(shotId)

// الحصول على جميع التسديدات
billiardSystem.getAllShots()
```

##### البحث والتصفية

```javascript
// البحث
billiardSystem.searchShots('query')

// التصفية حسب الجدران
billiardSystem.filterShotsByRails(2)

// التصفية حسب التاريخ
billiardSystem.filterShotsByDateRange(startDate, endDate)
```

##### الإحصائيات

```javascript
const stats = billiardSystem.getStatistics()
// النتيجة:
// {
//   total: 100,
//   successful: 75,
//   failed: 25,
//   successRate: '75.00',
//   avgSuccess: '72.50',
//   byRails: { 1: 10, 2: 30, 3: 40, 4: 20 },
//   bestShot: {...},
//   worstShot: {...}
// }
```

##### النسخ الاحتياطية

```javascript
// إنشاء نسخة احتياطية
billiardSystem.createBackup()

// استعادة نسخة احتياطية
billiardSystem.restoreBackup(backupId)

// قائمة النسخ الاحتياطية
billiardSystem.listBackups()
```

##### التصدير والاستيراد

```javascript
// تصدير البيانات
billiardSystem.exportData()

// استيراد البيانات
billiardSystem.importData(fileInput)

// مسح جميع البيانات
billiardSystem.clearAllData()
```

##### الحسابات

```javascript
// حساب نسبة النجاح
const rate = billiardSystem.calculateSuccessRate(angle, power, distance, difficulty)
// Returns: number (0-100)
```

---

## أمثلة الاستخدام

### مثال 1: استخدام أساسي

```javascript
// تهيئة النظام
const system = new BilliardsSystem()

// إضافة تسديدة
system.addShot({
  rails: 2,
  whiteBall: 5,
  target: 3,
  angle: 30,
  power: 60,
  distance: 150,
  difficulty: 2
})

// عرض الإحصائيات
console.log(system.getStatistics())
```

### مثال 2: البحث والتصفية

```javascript
// البحث عن تسديدات معينة
const results = system.searchShots('rails:2')

// الحصول على تسديدات الجدار 2
const rail2Shots = system.filterShotsByRails(2)

// الحصول على تسديدات اليوم
const today = new Date()
today.setHours(0, 0, 0, 0)
const tomorrow = new Date(today)
tomorrow.setDate(tomorrow.getDate() + 1)

const todayShoots = system.filterShotsByDateRange(today, tomorrow)
```

### مثال 3: إدارة النسخ الاحتياطية

```javascript
// إنشاء نسخة احتياطية تلقائية
system.createBackup()

// قائمة النسخ الاحتياطية
const backups = system.listBackups()
console.log(backups)

// استعادة نسخة قديمة
if (backups.length > 0) {
  system.restoreBackup(backups[0].id)
}
```

### مثال 4: التصدير والاستيراد

```javascript
// تصدير البيانات
system.exportData()
// سيحمل ملف JSON تلقائياً

// استيراد من ملف
document.getElementById('fileInput').addEventListener('change', (e) => {
  system.importData(e.target.files[0])
})
```

### مثال 5: تغيير الموضوع

```javascript
// الحصول على مدير الموضوع
const theme = system.theme

// تبديل الموضوع
theme.toggleTheme()

// تعيين موضوع معين
theme.setTheme('light')
theme.setTheme('dark')
```

---

## رموز الخطأ

| الرمز | الوصف |
|------|-------|
| `STORAGE_ERROR` | خطأ في التخزين |
| `IMPORT_ERROR` | خطأ في الاستيراد |
| `EXPORT_ERROR` | خطأ في التصدير |
| `BACKUP_ERROR` | خطأ في النسخة الاحتياطية |

---

## الثوابت

```javascript
// مفتاح التخزين الموحد
const STORAGE_KEY = '5a-diamond-system-data'

// إصدار API
const API_VERSION = '3.0.0'

// عدد النسخ الاحتياطية المحفوظة
const MAX_BACKUPS = 10

// عدد التسديدات الأقصى
const MAX_SHOTS = 10000
```

---

## الأحداث

النظام يدعم الأحداث التالية:

```javascript
// عند إضافة تسديدة
document.addEventListener('shot-added', (e) => {
  console.log('تم إضافة تسديدة:', e.detail)
})

// عند حذف تسديدة
document.addEventListener('shot-deleted', (e) => {
  console.log('تم حذف تسديدة:', e.detail)
})

// عند تحديث البيانات
document.addEventListener('data-updated', (e) => {
  console.log('تم تحديث البيانات:', e.detail)
})
```

---

## أفضل الممارسات

1. **حفظ البيانات بانتظام**
   ```javascript
   setInterval(() => system.createBackup(), 3600000) // كل ساعة
   ```

2. **التعامل مع الأخطاء**
   ```javascript
   try {
     system.addShot(shotData)
   } catch (error) {
     NotificationManager.show('❌ خطأ: ' + error.message, 'error')
   }
   ```

3. **استخدام النسخ الاحتياطية**
   ```javascript
   window.addEventListener('beforeunload', () => {
     system.createBackup()
   })
   ```

4. **مراقبة الأداء**
   ```javascript
   PerformanceManager.measureFunction('addShot', () => {
     system.addShot(shotData)
   })
   ```

---

## الدعم والمساعدة

للمزيد من المعلومات، راجع:
- [USER_GUIDE_AR.md](USER_GUIDE_AR.md) - دليل المستخدم
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - دليل المطور

---

**آخر تحديث**: يناير 2026
**الإصدار**: 3.0.0
**الحالة**: جاهز للإنتاج ✅
