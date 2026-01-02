#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 سكريبت تصحيح الأخطاء الإملائية
يقوم بتصحيح الأخطاء الشائعة في جميع الملفات
"""

import os
import re
from pathlib import Path

# قائمة التصحيحات
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

# الملفات المراد تصحيحها
EXTENSIONS = ['.py', '.js', '.html', '.md', '.json', '.css']

def fix_typos_in_file(file_path):
    """تصحيح الأخطاء في ملف واحد"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = 0
        
        for typo, correct in CORRECTIONS.items():
            pattern = re.compile(re.escape(typo), re.IGNORECASE)
            content, count = pattern.subn(correct, content)
            changes += count
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes
        return False, 0
        
    except Exception as e:
        return False, 0

def main():
    """تشغيل التصحيح على جميع الملفات"""
    base_path = Path('.')
    
    print("=" * 70)
    print("🔧 برنامج تصحيح الأخطاء الإملائية")
    print("=" * 70)
    
    total_files = 0
    total_corrections = 0
    corrected_files = []
    
    for file_path in base_path.rglob('*'):
        if file_path.is_file() and file_path.suffix in EXTENSIONS:
            success, changes = fix_typos_in_file(str(file_path))
            
            if success:
                corrected_files.append((str(file_path.relative_to(base_path)), changes))
                total_files += 1
                total_corrections += changes
                print(f"✅ {file_path.name}: {changes} تصحيح")
    
    print("\n" + "=" * 70)
    print(f"📊 النتائج:")
    print(f"  • عدد الملفات المصححة: {total_files}")
    print(f"  • إجمالي التصحيحات: {total_corrections}")
    
    if corrected_files:
        print(f"\n📝 الملفات المصححة:")
        for file_name, changes in corrected_files:
            print(f"  • {file_name}: {changes} تصحيح")
    
    print("\n" + "=" * 70)
    print("✅ تم إكمال التصحيح بنجاح!")

if __name__ == '__main__':
    main()
