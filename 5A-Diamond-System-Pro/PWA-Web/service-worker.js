// ==========================================
// Service Worker للتطبيق
// ==========================================

const CACHE_NAME = 'billiards-app-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/unified-app.html',
    '/css/style.css',
    '/js/main.js',
    '/js/system-services.js',
    '/js/integrated-system.js',
    '/manifest.json'
];

// تثبيت (Install)
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('تثبيت Cache');
                return cache.addAll(urlsToCache);
            })
    );
    self.skipWaiting();
});

// تفعيل (Activate)
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('حذف Cache قديم:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// جلب البيانات (Fetch)
self.addEventListener('fetch', (event) => {
    // للطلبات غير GET، دع المتصفح يتعامل معها مباشرة
    if (event.request.method !== 'GET') {
        return;
    }
    
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // إذا وجدنا النسخة المخبئة، أعدها
                if (response) {
                    return response;
                }
                
                // وإلا، اطلب من الشبكة
                return fetch(event.request)
                    .then((response) => {
                        // لا تخزن الطلبات غير الناجحة
                        if (!response || response.status !== 200 || response.type === 'basic' && !response.url.includes('api')) {
                            return response;
                        }
                        
                        // انسخ الرد
                        const responseToCache = response.clone();
                        caches.open(CACHE_NAME)
                            .then((cache) => {
                                cache.put(event.request, responseToCache);
                            });
                        
                        return response;
                    })
                    .catch(() => {
                        // إذا فشلت الشبكة والطلب، حاول الحصول على نسخة مخزنة
                        return caches.match('/index.html');
                    });
            })
    );
});

// معالجة الرسائل الخلفية
self.addEventListener('message', (event) => {
    console.log('رسالة من العميل:', event.data);
    
    if (event.data.action === 'skipWaiting') {
        self.skipWaiting();
    }
    
    if (event.data.action === 'clearCache') {
        caches.delete(CACHE_NAME);
    }
});

// الإخطارات (Push Notifications)
self.addEventListener('push', (event) => {
    if (!event.data) {
        return;
    }
    
    const data = event.data.json();
    const options = {
        body: data.body || 'تحديث جديد',
        icon: '/assets/icon-192x192.png',
        badge: '/assets/badge-72x72.png'
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title || 'البلياردو Pro', options)
    );
});

// النقر على الإخطار
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    event.waitUntil(
        clients.matchAll({ type: 'window' }).then((clientList) => {
            for (let i = 0; i < clientList.length; i++) {
                const client = clientList[i];
                if (client.url === '/' && 'focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow('/');
            }
        })
    );
});
