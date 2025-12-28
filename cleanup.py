#!/usr/bin/env python3
"""
سكريبت تنظيف المشروع
يحذف الملفات القديمة والمكررة بشكل آمن
"""

import os
from pathlib import Path

# الملفات المراد حذفها
files_to_remove = [
    "calculator.py",
    "engine.py",
    "rail_system.py",
    "shot.py",
    "statistics.py",
    "measurement.py",
    "calculator_improved.py",
    "engine_improved.py",
    "rail_system_improved.py",
    "main_improved.py",
    "check-project.js",
    "test-runner.js",
    "generate_icons.py",
    "billiards-system.css",
    "performance-service.js",
    "error-handler-service.js",
    "backup-service.js",
    "advanced-search-service.js",
    "rail-positions-system.js",
    "measurements-system.js",
    "main.py",
    "server.py",
    "settings.py",
]

root_dir = Path("/workspaces/codespaces-django")

print("🗑️  بدء تنظيف المشروع...")
print("=" * 60)

removed_count = 0
for file in files_to_remove:
    file_path = root_dir / file
    if file_path.exists():
        try:
            file_path.unlink()
            print(f"✅ تم حذف: {file}")
            removed_count += 1
        except Exception as e:
            print(f"❌ خطأ في حذف {file}: {e}")
    else:
        print(f"⏭️ الملف غير موجود: {file}")

print("=" * 60)
print(f"✨ تم حذف {removed_count} ملف")
print("🎉 تم تنظيف المشروع بنجاح!")
