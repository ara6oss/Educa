from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    
    STUDENT = 'student'
    TEACHER = 'teacher'

    STATUS_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]
    
    
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pic', default="default.jpg")
    bio= models.TextField()
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default=STUDENT)
    
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        
    
    
    def __str__(self) -> str:
        return self.user.username
        
    # def save(self, *args, **kwargs):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 100 or img.width > 100:
    #         new_img = (100, 100)
    #         img.thumbnail(new_img)
    #         img.save(self.image.path)