from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']  # 'auth_provider', 'created_at']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
