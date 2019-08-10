"""ProjectSmaple URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from channelsApp import views
from users.views import CodeViewSet, UserViewSet, ObtainJSONWebToken, RestPasswd

router = DefaultRouter()
router.register(r'codes', CodeViewSet, base_name='codes'),
router.register(r'users', UserViewSet, base_name='users'),
router.register(r'resetpasswd', RestPasswd, base_name='resetpasswd'),

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"^", include(router.urls)),
    # 导入api文档，包括代码
    url(r'^docs', include_docs_urls(title='ProjectSample')),
    # jwt认证,自定义获取Token验证用户名和密码
    url(r'^obtain_jwt_auth/', ObtainJSONWebToken.as_view()),
    url(r'^refresh_jwt_token/', ObtainJSONWebToken.as_view()),
    url(r'^verify_jwt_token/', ObtainJSONWebToken.as_view()),
    # channels
    path('channels/', include('channelsApp.urls')),
    path('chat/', views.index),
    path('accounts/login/', LoginView.as_view()),
    path('accounts/logout/', logout),
]
