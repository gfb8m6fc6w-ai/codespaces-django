#!/bin/bash

# سكريبت تنظيف المشروع
# يحذف الملفات القديمة والمكررة

echo "🗑️ بدء تنظيف المشروع..."

# حذف ملفات Python المكررة والمحسنة
cd /workspaces/codespaces-django

files_to_remove=(
    "calculator.py"
    "engine.py"
    "rail_system.py"
    "shot.py"
    "statistics.py"
    "measurement.py"
    "calculator_improved.py"
    "engine_improved.py"
    "rail_system_improved.py"
    "main_improved.py"
    "check-project.js"
    "test-runner.js"
    "generate_icons.py"
    "billiards-system.css"
    "performance-service.js"
    "error-handler-service.js"
    "backup-service.js"
    "advanced-search-service.js"
    "rail-positions-system.js"
    "measurements-system.js"
    "main.py"
    "server.py"
    "settings.py"
)

for file in "${files_to_remove[@]}"; do
    if [ -f "$file" ]; then
        rm -f "$file"
        echo "✅ تم حذف: $file"
    fi
done

echo "✨ تم تنظيف المشروع بنجاح!"
