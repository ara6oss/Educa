from django.db import models
from django.contrib.auth.models import User
from .fields import OrderField
from PIL import Image
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Ссылка")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категорий"

        ordering = ['title']
        
    def __str__(self):
        return self.title
        
class Lesson(models.Model):
    owner = models.ForeignKey(User, related_name="lesson_created", on_delete=models.CASCADE, verbose_name="Владелец")
    title = models.CharField(max_length=250, verbose_name="Название")
    image = models.ImageField(upload_to='images/', verbose_name="Картинка")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  related_name="lesson", verbose_name='Категория')
    overview = models.TextField()
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Ссылка")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    students = models.ManyToManyField(User, blank=True, related_name="lesson_joined", verbose_name="Ученики")
    class Meta:
        ordering = ['-created']
        
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title
    
        
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)
    

#         @admin.register(Subject)  админка
# class SubjectAdmin(admin.ModelAdmin):
#     list_display = ['title', 'slug']
#     prepopulated_fields = {"slug": ('title',)}

class Module(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="modules", on_delete=models.CASCADE, verbose_name="Урок")
    image = models.ImageField(upload_to='images/', verbose_name="Картинка")
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    order = OrderField(blank=True, for_fields=['lesson'])
    slug = models.SlugField(max_length=200, verbose_name="Ссылка")
    
    
    class Meta:
        ordering = ['order']
        
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"
    
    def __str__(self) -> str:
        return f'{self.order}, {self.title}'
    
    
class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, verbose_name="Модуль")
    order = OrderField(blank=True, for_fields=['module'])
    text = models.TextField(verbose_name="Текст", blank=True, null=True)
    image = models.ImageField(upload_to='images/', verbose_name="Картинка", blank=True, null=True)
    file = models.FileField(upload_to='files', verbose_name="Файл", blank=True, null=True)
    video = models.URLField(verbose_name="Видео", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контенты"
        
        
    
