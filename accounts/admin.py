from django.contrib import admin

from .models import User

# Register your models here.


# admin 관리자 창에서 지정된 목록을 카테고리 별로 확인할 수 있게 해주는 것들
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 여기에 쓰인 목록의 순서대로 값들이 노출 된다.
    list_display = ['username', 'email', 'website_url',
                    'is_active', 'is_staff', 'is_superuser']
