"""myblogapp URL Configuration

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
from django.urls import include, path
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('inuneko3/', include('inuneko3.urls')),
    #アプリケーションレベルURL設定。
    path('', include('django.contrib.auth.urls')),
    #ログイン 認証関連ビューの有効化。
    path('', auth_views.LoginView.as_view(template_name='inuneko3/login.html'), name='login'),
    #ログイン
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #ログアウト
]