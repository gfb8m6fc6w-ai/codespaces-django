#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تطبيق التصحيحات الشاملة
يصحح الأخطاء الإملائية ويدمج التغييرات
"""

import os
import json
from pathlib import Path
import re

# ==================== قائمة التصحيحات ====================

CORRECTIONS = {
    # الأخطاء الإملائية الرئيسية
    'التسديقات': 'التسديدات',
    'التسديقة': 'التسديدة',
    'التسديق': 'التسديد',
    'حفظ التسديقة': 'حفظ التسديدة',
    'تحميل التسديقات': 'تحميل التسديدات',
    'حساب التسديقات': 'حساب التسديدات',
    'نموذج التسديقة': 'نموذج التسديدة',
    'حاسبة التسديقات': 'حاسبة التسديدات',
}

# تحديث مفتاح التخزين
STORAGE_UPDATES = {
    'billiardsApp_data': '5a-diamond-system-data',
    'STORAGE_KEY = \'billiardsApp_data\'': 'STORAGE_KEY = \'5a-diamond-system-data\'',
}

# ==================== الملفات المستهدفة ====================

TARGET_FILES = [
    # Python files
    'pythonista_advanced_billiards.py',
    'pythonista_billiards_app.py',
    '5A-Diamond-System-Pro/Pythonista-iOS/billiards_app.py',
    '5A-Diamond-System-Pro/Pythonista-iOS/billiards_app_advanced.py',
    'pythonista/pythonista_advanced_billiards.py',
    'pythonista/pythonista_billiards_app.py',
    
    # JavaScript files
    'script.js',
    'unified-app.html',
    '5A-Diamond-System-Pro/PWA-Web/js/main.js',
    'billiards-engine.js',
    'integrated-shot-system.js',
    'system-services.js',
    
    # JSON files
    '5A-Diamond-System-Pro/Shared-Core/config.json',
    'manifest.json',
]

# ==================== دوال المعالجة ====================

def apply_corrections_to_file(file_path, corrections, storage_updates):
    """تطبيق التصحيحات على ملف واحد"""
    try:
        if not os.path.exists(file_path):
            return False, f"الملف غير موجود: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        # تطبيق التصحيحات الإملائية
        for wrong, correct in corrections.items():
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            content, count = pattern.subn(correct, content)
            changes += count
        
        # تطبيق تحديثات التخزين
        for old_key, new_key in storage_updates.items():
            pattern = re.compile(re.escape(old_key))
            content, count = pattern.subn(new_key, content)
            changes += count
        
        # حفظ الملف إذا حدثت تغييرات
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"✅ تم التصحيح: {changes} تغيير"
        else:
            return False, "لا توجد تغييرات مطلوبة"
            
    except Exception as e:
        return False, f"❌ خطأ: {str(e)}"

def main():
    """تشغيل التصحيحات على جميع الملفات"""
    base_path = Path(__file__).parent
    
    results = {
        'success': [],
        'skipped': [],
        'errors': []
    }
    
    print("=" * 60)
    print("🔧 بدء تطبيق التصحيحات الشاملة")
    print("=" * 60)
    
    for file_rel in TARGET_FILES:
        file_path = base_path / file_rel
        
        print(f"\n📄 معالجة: {file_rel}")
        
        success, message = apply_corrections_to_file(
            str(file_path),
            CORRECTIONS,
            STORAGE_UPDATES
        )
        
        if success:
            print(f"   {message}")
            results['success'].append(file_rel)
        elif message.startswith("لا"):
            print(f"   ⏭️  {message}")
            results['skipped'].append(file_rel)
        else:
            print(f"   {message}")
            results['errors'].append(file_rel)
    
    # الملخص
    print("\n" + "=" * 60)
    print("📊 ملخص النتائج")
    print("=" * 60)
    print(f"✅ الملفات المصححة: {len(results['success'])}")
    print(f"⏭️  الملفات المتجاهلة: {len(results['skipped'])}")
    print(f"❌ الملفات بها أخطاء: {len(results['errors'])}")
    
    if results['success']:
        print("\n✅ الملفات المصححة:")
        for f in results['success']:
            print(f"   - {f}")
    
    if results['errors']:
        print("\n❌ الملفات بها أخطاء:")
        for f in results['errors']:
            print(f"   - {f}")
    
    return len(results['errors']) == 0

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
