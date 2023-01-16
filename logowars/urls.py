"""logowars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based viewspy
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('loginsuccess/', views.loginsuccess, name='loginsuccess'),
    path('loginsuccess/mylogo/', views.mylogo, name='mylogo'),
    path('loginsuccess/mylogo/upload', views.upload, name='upload'),
    path('loginsuccess/mylogo/auction', views.BidUpload, name='BidUpload'),
    path('loginsuccess/view', views.view, name='view'),
    path('loginsuccess/view/bid+100', views.bid_increase, name='bid_increase'),
    path('logout/', views.logout, name='logout'),
    path('loginsuccess/editprofile', views.edit_profile, name='edit_profile'),
    path('loginsuccess/mybids', views.mybids, name='mybids'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
