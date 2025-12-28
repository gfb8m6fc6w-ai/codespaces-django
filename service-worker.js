/*
 * Service Worker - العامل الخدمي
 * يوفر: الـ Caching، العمل Offline، Push Notifications
 * 
 * الميزات:
 * - تخزين مؤقت ذكي (Cache First / Network First)
 * - العمل بدون انترنت
 * - تحديث البيانات في الخلفية
 * - معالجة الأخطاء
 */

const CACHE_NAME = 'billiards-app-v2.0.0';
const RUNTIME_CACHE = 'billiards-runtime-v2.0.0';
const IMAGES_CACHE = 'billiards-images-v2.0.0';

// الملفات الأساسية التي يجب تخزينها مؤقتاً عند التثبيت
const STATIC_ASSETS = [
  '/',
  '/app/',
  '/frontend/html/unified-app.html',
  '/frontend/css/main.css',
  '/frontend/css/style-pwa.css',
  '/static/main.css',
  '/manifest.json',
];

/**
 * 1. حدث التثبيت (Installation Event)
 * يتم تنشيط هذا الحدث عند تثبيت Service Worker لأول مرة
 */
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker: جاري التثبيت...');
  
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('📦 Service Worker: تخزين الملفات الأساسية');
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('⚠️ تحذير: بعض الملفات لم تُخزن', err);
      });
    })
  );
  
  // فرض استبدال إصدار قديم بالجديد فوراً
  self.skipWaiting();
});

/**
 * 2. حدث التفعيل (Activation Event)
 * يتم تنشيط هذا الحدث بعد تثبيت Service Worker بنجاح
 */
self.addEventListener('activate', (event) => {
  console.log('✅ Service Worker: جاري التفعيل...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // حذف النسخ القديمة من الـ Cache
          if (cacheName !== CACHE_NAME && 
              cacheName !== RUNTIME_CACHE && 
              cacheName !== IMAGES_CACHE) {
            console.log(`🗑️ حذف cache قديم: ${cacheName}`);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  
  // السيطرة على جميع العملاء الحالية فوراً
  self.clients.claim();
});

/**
 * 3. حدث Fetch - معالجة طلبات الشبكة
 * استراتيجية مختلفة حسب نوع الملف
 */
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);
  
  // تجاهل الطلبات غير HTTP/HTTPS
  if (!url.protocol.startsWith('http')) {
    return;
  }
  
  // 1. لطلبات الملفات الثابتة (HTML, CSS, JS)
  if (request.method === 'GET' && isStaticAsset(url.pathname)) {
    event.respondWith(
      caches.match(request).then((response) => {
        // إذا كانت في الـ Cache، أرجعها فوراً
        if (response) {
          console.log(`✅ Cache Hit: ${url.pathname}`);
          return response;
        }
        
        // وإلا حاول من الشبكة
        console.log(`🌐 Network Fetch: ${url.pathname}`);
        return fetch(request).then((response) => {
          // إذا كانت الاستجابة ناجحة، احفظها
          if (response.status === 200) {
            const responseToCache = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, responseToCache);
            });
          }
          return response;
        }).catch(() => {
          // إذا فشلت الشبكة، عد إلى fallback
          return new Response('متاح بدون اتصال', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: new Headers({
              'Content-Type': 'text/plain'
            })
          });
        });
      })
    );
    return;
  }
  
  // 2. لطلبات الصور
  if (request.method === 'GET' && isImage(url.pathname)) {
    event.respondWith(
      caches.match(request).then((response) => {
        if (response) {
          return response;
        }
        
        return fetch(request).then((response) => {
          if (response.status === 200) {
            const responseToCache = response.clone();
            caches.open(IMAGES_CACHE).then((cache) => {
              cache.put(request, responseToCache);
            });
          }
          return response;
        }).catch(() => {
          // صورة بديلة في حالة الفشل
          return new Response('<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect fill="#ddd" width="100" height="100"/></svg>', {
            headers: { 'Content-Type': 'image/svg+xml' }
          });
        });
      })
    );
    return;
  }
  
  // 3. لطلبات API
  if (request.method === 'GET' && isAPI(url.pathname)) {
    event.respondWith(
      fetch(request).then((response) => {
        if (response.status === 200) {
          const responseToCache = response.clone();
          caches.open(RUNTIME_CACHE).then((cache) => {
            cache.put(request, responseToCache);
          });
        }
        return response;
      }).catch(() => {
        // محاولة إرجاع من الـ Cache
        return caches.match(request).then((response) => {
          if (response) {
            console.log(`📦 استخدام cached API response: ${url.pathname}`);
            return response;
          }
          
          return new Response(JSON.stringify({ 
            error: 'لا يمكن الوصول للخادم',
            offline: true 
          }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
          });
        });
      })
    );
    return;
  }
  
  // 4. بقية الطلبات (Network First)
  event.respondWith(
    fetch(request).then((response) => {
      if (response.status === 200) {
        const responseToCache = response.clone();
        caches.open(RUNTIME_CACHE).then((cache) => {
          cache.put(request, responseToCache);
        });
      }
      return response;
    }).catch(() => {
      return caches.match(request).catch(() => {
        return new Response('متاح بدون اتصال', {
          status: 503,
          headers: { 'Content-Type': 'text/plain' }
        });
      });
    })
  );
});

/**
 * 4. معالجة Sync Events (Background Sync)
 * مزامنة البيانات عندما يعود الاتصال
 */
self.addEventListener('sync', (event) => {
  console.log('🔄 Background Sync:', event.tag);
  
  if (event.tag === 'sync-shots') {
    event.waitUntil(syncShotsData());
  }
  
  if (event.tag === 'sync-statistics') {
    event.waitUntil(syncStatisticsData());
  }
});

/**
 * 5. معالجة Push Notifications
 */
self.addEventListener('push', (event) => {
  console.log('📢 Push notification:', event);
  
  if (!event.data) {
    return;
  }
  
  const options = {
    body: event.data.text(),
    icon: '/images/icon-192x192.png',
    badge: '/images/badge-72x72.png',
    tag: 'billiards-notification',
    requireInteraction: false,
    actions: [
      {
        action: 'open-app',
        title: 'فتح التطبيق'
      },
      {
        action: 'close',
        title: 'إغلاق'
      }
    ]
  };
  
  event.waitUntil(self.registration.showNotification('نظام البلياردو', options));
});

/**
 * 6. معالجة النقرات على الإشعارات
 */
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'open-app' || !event.action) {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then((clientList) => {
        // إذا كان التطبيق مفتوح، عد إليه
        for (let client of clientList) {
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        // وإلا افتح نافذة جديدة
        if (clients.openWindow) {
          return clients.openWindow('/app/');
        }
      })
    );
  }
});

/**
 * وظائف مساعدة
 */

function isStaticAsset(pathname) {
  return /\.(html|css|js|json|woff|woff2|ttf|otf)$/i.test(pathname) ||
         pathname.endsWith('/') ||
         pathname === '' ||
         pathname === '/app/';
}

function isImage(pathname) {
  return /\.(png|jpg|jpeg|gif|webp|svg|ico)$/i.test(pathname);
}

function isAPI(pathname) {
  return pathname.startsWith('/api/') || 
         pathname.startsWith('/billiards/') ||
         pathname.startsWith('/statistics/');
}

async function syncShotsData() {
  try {
    const db = await openDatabase();
    const unsynced = await getUnsyncedShots(db);
    
    if (unsynced.length > 0) {
      const response = await fetch('/api/v1/sync-shots', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ shots: unsynced })
      });
      
      if (response.ok) {
        await markShotsAsSynced(db, unsynced);
      }
    }
  } catch (error) {
    console.error('خطأ في المزامنة:', error);
    throw error;
  }
}

async function syncStatisticsData() {
  try {
    const db = await openDatabase();
    const stats = await getStatistics(db);
    
    await fetch('/api/v1/sync-statistics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ statistics: stats })
    });
  } catch (error) {
    console.error('خطأ في مزامنة الإحصائيات:', error);
    throw error;
  }
}

async function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('BilliardsDB', 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
  });
}

// ملخص السجل
console.log('✨ Service Worker تم تحميله - الإصدار 2.0.0');
console.log('📋 الميزات:');
console.log('  ✅ Offline Support');
console.log('  ✅ Smart Caching');
console.log('  ✅ Background Sync');
console.log('  ✅ Push Notifications');
