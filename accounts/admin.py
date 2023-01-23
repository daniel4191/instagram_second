from django.contrib import admin

from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # list_display 자체가가 admin.ModelAdmin에 내장되어있는 기능이며
    # admin 화면으로 볼때의 카테고리 표시를 의미한다.
    list_display = ['username', 'email', 'website_url','is_staff' ,'is_superuser']