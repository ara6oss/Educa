from django.contrib import admin
from django.urls import path
from lessons import views
app_name = 'lessons'
urlpatterns = [
    # path('search/', views.catalog, name='search'),
    path('<slug:category_slug>', views.home, name='index'),
    path('course/<slug:course_slug>/', views.course_detail, name='course_detail')
]
