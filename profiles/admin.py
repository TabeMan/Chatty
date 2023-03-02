from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'username', 'first_name',
                    'last_name', 'email', 'profile_image', 'updated', 'created']
    prepopulated_fields = {'slug': ('username',)}
    raw_id_fields = ['user']
