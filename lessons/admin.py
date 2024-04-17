from django.contrib import admin
from django import forms
from lessons.models import Category, Lesson, Module, Content
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.


class ContentInline(admin.StackedInline):
    model=Content

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson']
    list_filter = ['lesson']
    search_fields = ['title', 'lesson']
    inlines = [ContentInline]



class ModuleInline(admin.StackedInline):
    model=Module

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {"slug": ('title',)}
    
    
class OverviewLessonForm(forms.ModelForm):
    overview = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Lesson
        fields = '__all__'
    


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created']
    list_filter = ['created', 'category']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    form = OverviewLessonForm
    inlines = [ModuleInline]
    
    


admin.site.register(Content)