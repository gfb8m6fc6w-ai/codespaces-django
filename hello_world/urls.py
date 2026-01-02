"""
URL configuration for hello_world project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from hello_world.core import views as core_views

# Health check endpoint للـ iPad
@require_http_methods(["GET", "HEAD"])
def health_check(request):
    """فحص صحة الخادم"""
    return JsonResponse({
        'status': 'ok',
        'message': 'الخادم يعمل بنجاح ✅',
        'debug': settings.DEBUG,
    })

urlpatterns = [
    path("", core_views.index),
    path("health/", health_check, name="health"),
    path("api/health/", health_check, name="api_health"),
    path("api/info/", core_views.api_info, name="api_info"),
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
