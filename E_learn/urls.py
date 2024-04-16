"""
URL configuration for E_learn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from students.views import *
from lessons.views import *
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name='home'),
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(template_name='students/logout.html'), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('profile/', profile, name='profile'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='students/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='students/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/update/', update_profile, name='update_profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    
    path('lesson/', include('lessons.urls', namespace='lesson')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
