from django.contrib import admin
from django.urls import path
from lessons import views
app_name = 'lessons'
urlpatterns = [
    path('search/', views.home, name='search'),
    path('<slug:category_slug>', views.home, name='index'),
    path('course/<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:course_slug>/<slug:module_slug>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('course/<slug:course_slug>/<slug:module_slug>/like', views.AddLike.as_view(), name='like'),
    path('course/<slug:course_slug>/<slug:module_slug>/dislike', views.AddDislike.as_view(), name='dislike'),
    
]
