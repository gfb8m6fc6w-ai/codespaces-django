#!/usr/bin/env node

/**
 * 🧪 فاحص المشروع السريع
 * يتحقق من وجود جميع الملفات المطلوبة
 */

const fs = require('fs');
const path = require('path');

// الألوان للـ console
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

const log = {
  success: msg => console.log(`${colors.green}✅ ${msg}${colors.reset}`),
  error: msg => console.log(`${colors.red}❌ ${msg}${colors.reset}`),
  warning: msg => console.log(`${colors.yellow}⚠️ ${msg}${colors.reset}`),
  info: msg => console.log(`${colors.blue}ℹ️ ${msg}${colors.reset}`),
  header: msg => console.log(`\n${colors.cyan}${msg}${colors.reset}\n`)
};

// قائمة الملفات المتوقعة
const expectedFiles = {
  'الملفات الأساسية الأصلية': [
    'index.html',
    'style.css',
    'script.js',
    'sw.js',
    'manifest.json'
  ],
  'الملفات الأصلية الإضافية': [
    'rail-positions-system.js',
    'measurements-system.js',
    'geometry-calculator.js',
    'validation-engine.js',
    'performance-optimizer.js'
  ],
  'الملفات الجديدة - Core': [
    'core/billiards-engine.js',
    'ui/unified-app.html'
  ],
  'الملفات الجديدة - Services': [
    'services/system-services.js',
    'services/error-handler-service.js',
    'services/performance-service.js',
    'services/advanced-search-service.js',
    'services/backup-service.js'
  ],
  'الملفات الجديدة - Tests': [
    'tests/test-runner.js'
  ],
  'ملفات التوثيق - Docs': [
    'docs/README-COMPLETE.md',
    'docs/ARCHITECTURE.md',
    'docs/RESTRUCTURING-SUMMARY.md'
  ],
  'ملفات التوثيق - Root': [
    'README.md',
    '🔧-ISSUES-FIXES-IMPROVEMENTS.md',
    '📋-SOLUTIONS-SUMMARY.md',
    '🔗-INTEGRATION-GUIDE.md',
    '📊-COMPREHENSIVE-FINAL-SUMMARY.md',
    '📥-UPLOAD-DOWNLOAD-GUIDE.md',
    '✅-READY-TO-UPLOAD.md'
  ],
  'سكريبتات الرفع': [
    'final-upload.sh',
    'git-push.py',
    '📤-MANUAL-UPLOAD-STEPS.md',
    '🎬-VIDEO-GUIDE-QUICK-UPLOAD.md'
  ]
};

// الدالة الرئيسية
function checkProject() {
  const projectRoot = process.cwd();
  
  console.clear();
  log.header('🧪 فاحص المشروع - تحقق شامل');
  console.log(`📁 المجلد: ${projectRoot}\n`);
  
  let totalFiles = 0;
  let foundFiles = 0;
  let missingFiles = [];
  
  // التحقق من كل فئة
  for (const [category, files] of Object.entries(expectedFiles)) {
    log.header(`📂 ${category}`);
    
    let categoryFound = 0;
    
    files.forEach(file => {
      const filePath = path.join(projectRoot, file);
      totalFiles++;
      
      if (fs.existsSync(filePath)) {
        const stats = fs.statSync(filePath);
        const size = (stats.size / 1024).toFixed(2);
        log.success(`${file} (${size} KB)`);
        categoryFound++;
        foundFiles++;
      } else {
        log.error(`${file} (غير موجود)`);
        missingFiles.push(file);
      }
    });
    
    console.log(`\n📊 ${categoryFound}/${files.length} ملفات موجودة\n`);
  }
  
  // الملخص النهائي
  console.log('\n' + '='.repeat(60));
  log.header('📊 الملخص النهائي');
  
  const percentage = ((foundFiles / totalFiles) * 100).toFixed(1);
  console.log(`📈 الملفات الموجودة: ${foundFiles}/${totalFiles} (${percentage}%)\n`);
  
  if (percentage === '100.0') {
    log.success('جميع الملفات موجودة! المشروع جاهز للرفع 🚀');
  } else if (percentage >= '90') {
    log.warning(`${missingFiles.length} ملف مفقود فقط`);
    console.log('الملفات المفقودة:');
    missingFiles.forEach(f => console.log(`  ❌ ${f}`));
  } else {
    log.error(`${missingFiles.length} ملف مفقود`);
  }
  
  // معلومات Git
  log.header('🔧 معلومات Git');
  
  const gitDir = path.join(projectRoot, '.git');
  if (fs.existsSync(gitDir)) {
    log.success('مستودع Git موجود');
    
    // حساب عدد commits
    try {
      const headFile = path.join(gitDir, 'HEAD');
      const ref = fs.readFileSync(headFile, 'utf-8').trim();
      log.info(`الفرع الحالي: ${ref}`);
    } catch (e) {
      log.warning('لم يتمكن من قراءة معلومات الفرع');
    }
  } else {
    log.error('مستودع Git غير موجود');
  }
  
  // إحصائيات المشروع
  log.header('📊 إحصائيات المشروع');
  
  let totalSize = 0;
  let jsFiles = 0;
  let htmlFiles = 0;
  let mdFiles = 0;
  
  function walkDir(dir) {
    const files = fs.readdirSync(dir);
    
    files.forEach(file => {
      if (file.startsWith('.')) return;
      
      const filePath = path.join(dir, file);
      const stats = fs.statSync(filePath);
      
      if (stats.isDirectory()) {
        walkDir(filePath);
      } else {
        totalSize += stats.size;
        
        if (file.endsWith('.js')) jsFiles++;
        if (file.endsWith('.html')) htmlFiles++;
        if (file.endsWith('.md')) mdFiles++;
      }
    });
  }
  
  try {
    walkDir(projectRoot);
    console.log(`📄 ملفات JavaScript: ${jsFiles}`);
    console.log(`🌐 ملفات HTML: ${htmlFiles}`);
    console.log(`📖 ملفات Markdown: ${mdFiles}`);
    console.log(`💾 إجمالي الحجم: ${(totalSize / 1024 / 1024).toFixed(2)} MB\n`);
  } catch (e) {
    log.warning('لم يتمكن من حساب الإحصائيات');
  }
  
  // التوصيات
  log.header('🎯 التوصيات التالية');
  
  if (percentage === '100.0') {
    console.log('1️⃣ المشروع مكتمل - جاهز للرفع على GitHub');
    console.log('2️⃣ استخدم GitHub Desktop أو VS Code للرفع');
    console.log('3️⃣ تحقق من github.com/5ASp/5A-SysPro بعد الرفع');
    console.log('4️⃣ شارك الرابط مع الآخرين\n');
  } else {
    console.log(`1️⃣ يوجد ${missingFiles.length} ملف مفقود - قم بإنشاؤها أولاً`);
    console.log('2️⃣ تحقق من المسارات والأسماء');
    console.log('3️⃣ جرّب نسخ الملفات من نسخة أخرى\n');
  }
  
  // معلومات الاتصال
  log.header('📞 معلومات مفيدة');
  
  console.log('🔗 رابط GitHub: https://github.com/5ASp/5A-SysPro');
  console.log('📖 دليل الرفع: 📤-MANUAL-UPLOAD-STEPS.md');
  console.log('🎬 فيديو شرح: 🎬-VIDEO-GUIDE-QUICK-UPLOAD.md\n');
  
  console.log('=' .repeat(60) + '\n');
  
  return percentage === '100.0' ? 0 : 1;
}

// تشغيل الفاحص
try {
  const code = checkProject();
  process.exit(code);
} catch (error) {
  log.error(`خطأ: ${error.message}`);
  process.exit(1);
}
