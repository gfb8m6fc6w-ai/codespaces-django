# 👨‍💻 دليل المطور
## نظام البلياردو المتقدم - 5A Diamond System Pro

---

## 📖 جدول المحتويات

1. [البنية المعمارية](#البنية-المعمارية)
2. [التثبيت والإعداد](#التثبيت-والإعداد)
3. [واجهات API](#واجهات-api)
4. [نماذج البيانات](#نماذج-البيانات)
5. [الخوارزميات](#الخوارزميات)
6. [المساهمة](#المساهمة)

---

## 🏗️ البنية المعمارية

```
5A-Diamond-System-Pro/
├── Pythonista-iOS/        # تطبيق iOS
├── PWA-Web/               # تطبيق الويب (Progressive Web App)
├── Python-Backend/        # الخادم الخلفي
├── Shared-Core/           # الملفات المشتركة
└── Documentation/         # الوثائق
```

### الطبقات:
1. **طبقة العرض (UI)**: HTML/CSS/JavaScript
2. **طبقة الأعمال (Logic)**: حسابات وتحليلات
3. **طبقة البيانات (Data)**: التخزين والقواعد البيانات
4. **طبقة API**: واجهات RESTful

---

## ⚙️ التثبيت والإعداد

### المتطلبات:
- Python 3.8+
- Node.js 14+ (اختياري للويب)
- Pythonista 3 (للهواتف)

### خطوات التثبيت:

```bash
# 1. استنساخ المستودع
git clone <repo-url>
cd 5A-Diamond-System-Pro

# 2. تثبيت المتطلبات
pip install -r Python-Backend/requirements.txt

# 3. تشغيل الخادم
python Python-Backend/api.py

# 4. فتح التطبيق
# الويب: http://localhost:8000
# أو افتح PWA-Web/index.html
```

---

## 🔌 واجهات API

### 1. حساب التسديقة

**الطلب:**
```http
POST /api/v1/calculate
Content-Type: application/json

{
    "angle": 0,
    "power": 50,
    "distance": 100,
    "difficulty": 2
}
```

**الاستجابة:**
```json
{
    "success": true,
    "shot": {
        "id": 1234567890,
        "angle": 0,
        "power": 50,
        "distance": 100,
        "difficulty": 2,
        "timestamp": "2024-01-02T10:30:00Z"
    },
    "success_rate": 75.5,
    "recommendation": "جيد جداً"
}
```

### 2. الحصول على الإحصائيات

**الطلب:**
```http
GET /api/v1/statistics
```

**الاستجابة:**
```json
{
    "total_shots": 150,
    "avg_success_rate": 68.5,
    "best_shot": {...},
    "worst_shot": {...},
    "last_shot": {...}
}
```

### 3. الحصول على قائمة التسديقات

**الطلب:**
```http
GET /api/v1/shots?skip=0&limit=50
```

**الاستجابة:**
```json
{
    "total": 150,
    "count": 50,
    "shots": [...]
}
```

---

## 📊 نماذج البيانات

### نموذج التسديقة (Shot)
```python
class Shot:
    angle: float          # -90 إلى 90
    power: float          # 0 إلى 100
    distance: float       # 0 إلى 500
    difficulty: int       # 0 إلى 5
    success_rate: float   # 0 إلى 100
    timestamp: str        # ISO 8601
    id: int              # معرف فريد
```

### نموذج الإحصائيات (Statistics)
```python
class Statistics:
    total_shots: int
    avg_success_rate: float
    best_shot: Shot
    worst_shot: Shot
    last_shot: Shot
    trend: str           # "تحسن" أو "تراجع" أو "مستقر"
```

---

## 🧮 الخوارزميات

### حساب نسبة النجاح

```python
def calculate_success_rate(angle, power, distance, difficulty):
    # تأثير الزاوية
    angle_factor = 100 - (abs(angle) / 90 * 50)
    
    # تأثير القوة
    if 40 <= power <= 70:
        power_factor = 100
    elif 20 <= power < 40:
        power_factor = 60 + (power - 20) * 2
    elif 70 < power <= 100:
        power_factor = 100 - (power - 70) * 1.5
    else:
        power_factor = max(0, power)
    
    # تأثير المسافة
    if distance <= 50:
        distance_factor = 100
    elif distance <= 200:
        distance_factor = 100 - (distance - 50) * 0.25
    else:
        distance_factor = 100 - (distance - 200) * 0.1
    
    # تأثير الصعوبة
    difficulty_factors = [150, 120, 100, 80, 60, 40]
    difficulty_factor = difficulty_factors[difficulty]
    
    # الحساب النهائي
    success_rate = (
        angle_factor * 0.25 +
        power_factor * 0.25 +
        distance_factor * 0.25 +
        difficulty_factor * 0.25
    )
    
    return min(100, max(0, success_rate))
```

### معاملات الصعوبة:
- **سهل جداً**: 1.5x
- **سهل**: 1.2x
- **متوسط**: 1.0x (القياسي)
- **صعب**: 0.8x
- **صعب جداً**: 0.6x
- **احترافي**: 0.4x

---

## 🤝 المساهمة

### خطوات المساهمة:

1. **فرع جديد:**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **قم بالتغييرات:**
   ```bash
   git add .
   git commit -m "وصف التغيير"
   ```

3. **أرسل الطلب:**
   ```bash
   git push origin feature/your-feature
   ```

4. **افتح Pull Request**

### معايير الكود:
- التعليقات بالعربية
- تنسيق PEP 8 (للـ Python)
- اختبارات شاملة
- توثيق كامل

---

## 📝 الترخيص

جميع الحقوق محفوظة © 2024

---

## 📞 التواصل

للأسئلة والاقتراحات:
- البريد الإلكتروني: support@billiardsapp.com
- GitHub Issues
- Discord Server

---

**شكراً لمساهمتك! 🙏**
