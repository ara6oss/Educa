from django.contrib import admin
from django.urls import path
from lessons import views
app_name = 'lessons'
urlpatterns = [
    path('search/', views.home, name='search'),
    path('course/liked_modules/', views.liked_modules, name='liked_modules'),
    path('course/view_comments/', views.view_comments, name='view_comments'),
    
    path('<slug:category_slug>', views.home, name='index'),
    path('course/<slug:course_slug>/', views.course_detail, name='course_detail'),
    path('course/<slug:course_slug>/save', views.AddSave.as_view(), name='save_playlist'),
    

    path('course/<slug:course_slug>/<slug:module_slug>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('course/<slug:course_slug>/<slug:module_slug>/like', views.AddLike.as_view(), name='like'),
    path('course/<slug:course_slug>/<slug:module_slug>/dislike', views.AddDislike.as_view(), name='dislike'),
    path('course/<slug:course_slug>/<slug:module_slug>/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('course/<slug:course_slug>/<slug:module_slug>/update/<int:comment_id>/', views.update_comment, name='update_comment'),
    path('course/<slug:course_slug>/<slug:module_slug>/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    

]
