from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
import platform
import sys

def index(request):
    """الصفحة الرئيسية"""
    context = {
        "title": "نظام البلياردو المتقدم 5A Diamond System Pro",
        "version": "2.0.0",
        "debug": settings.DEBUG,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "platform": platform.system(),
    }
    return render(request, "index.html", context)

def api_info(request):
    """نقطة نهاية API للحصول على معلومات التطبيق"""
    return JsonResponse({
        'app_name': 'نظام البلياردو المتقدم',
        'version': '2.0.0',
        'status': 'active',
        'features': [
            'حاسبة الضربات',
            'مدير القياسات',
            'نظام السكة الحديدية',
        ],
        'environment': {
            'debug': settings.DEBUG,
            'database': settings.DATABASES['default']['ENGINE'],
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}",
        }
    })
