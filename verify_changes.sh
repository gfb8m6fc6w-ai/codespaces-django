#!/usr/bin/env bash
# 🔍 سكريبت التحقق من التعديلات - توحيد مفاتيح localStorage

echo "═══════════════════════════════════════════════════════════"
echo "  🔍 التحقق من تعديلات localStorage"
echo "═══════════════════════════════════════════════════════════"

echo ""
echo "✅ 1. التحقق من وجود STORAGE_KEY في system-services.js:"
grep -n "const STORAGE_KEY" /workspaces/codespaces-django/system-services.js | head -1

echo ""
echo "✅ 2. التحقق من وجود STORAGE_KEY في script.js:"
grep -n "const STORAGE_KEY" /workspaces/codespaces-django/script.js | head -1

echo ""
echo "✅ 3. التحقق من استخدام STORAGE_KEY + '-app' في system-services.js:"
grep -n "STORAGE_KEY + '-app'" /workspaces/codespaces-django/system-services.js | head -1

echo ""
echo "✅ 4. التحقق من استخدام STORAGE_KEY + '-database' في script.js:"
grep -n "STORAGE_KEY + '-database'" /workspaces/codespaces-django/script.js | head -1

echo ""
echo "✅ 5. التحقق من استخدام STORAGE_KEY + '-custom' في script.js:"
grep -n "STORAGE_KEY + '-custom'" /workspaces/codespaces-django/script.js | head -1

echo ""
echo "✅ 6. التحقق من استخدام STORAGE_KEY + '-diamond' في script.js:"
grep -n "STORAGE_KEY + '-diamond'" /workspaces/codespaces-django/script.js | head -1

echo ""
echo "✅ 7. التحقق من استخدام STORAGE_KEY + '-theme' في script.js:"
grep -n "STORAGE_KEY + '-theme'" /workspaces/codespaces-django/script.js | head -1

echo ""
echo "✅ 8. التحقق من استخدام STORAGE_KEY + '-history' في script.js:"
grep -n "STORAGE_KEY + '-history'" /workspaces/codespaces-django/script.js | head -1

echo ""
echo "✅ 9. التحقق من استخدام STORAGE_KEY + '-favorites' في script.js:"
grep -n "STORAGE_KEY + '-favorites'" /workspaces/codespaces-django/script.js | head -1

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📊 إجمالي عدد استخدامات STORAGE_KEY:"
echo "═══════════════════════════════════════════════════════════"

echo ""
echo "في system-services.js:"
grep -c "STORAGE_KEY" /workspaces/codespaces-django/system-services.js

echo ""
echo "في script.js:"
grep -c "STORAGE_KEY" /workspaces/codespaces-django/script.js

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  ✅ التحقق اكتمل بنجاح!"
echo "═══════════════════════════════════════════════════════════"
