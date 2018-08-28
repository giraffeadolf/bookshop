"""bookshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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

from django.urls import path
import mainapp.views as mainapp
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('', mainapp.main, name='main'),
    path('contact/', mainapp.contact, name='contact'),
    path('catalog/', include('mainapp.urls', namespace='catalog')),
    path('shares/', mainapp.shares, name='shares'),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('auth/', include('authapp.urls', namespace='auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
