"""
URL configuration for ComandProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf.urls.static import static

from ComandProject import settings
from ProductService import views as main_views
from account import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.HomePageView.as_view(), name='home'),
    path('login/', account_views.LoginView.as_view(), name='login'),
    path('logout/', account_views.LogoutView.as_view(), name='logout'),
    path('register/', account_views.RegisterView.as_view(), name='register'),
    path('profile/', account_views.ProfileView.as_view(), name='profile'),
    path('app/', include('ProductService.urls')),
    path('payment/', include('orders.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
