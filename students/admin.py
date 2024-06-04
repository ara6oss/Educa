from django.contrib import admin

from students.models import Profile

# Register your models here.
# admin.site.register(Profile)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'bio')
    list_filter = ('status',)
    search_fields = ('user__username', 'bio')