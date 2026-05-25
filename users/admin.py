from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


class CustomUserAdmin(UserAdmin):
    model=User
    list_display=['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined']
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    
    search_fields = ('email', 'first_name', 'last_name')
    ordering=('email',)

    fieldsets=(
        (None, {'fields':('email','password')}),
        ('personal Info', {'fields':('first_name','last_name')}),
        ('Permissions', {'fields':('is_staff','is_active','is_superuser','groups','user_permissions')}),
        ('Important Dates', {'fields':('last_login','date_joined')})
    )

    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('email','password1','password2','is_staff','is_active')   
        }),
    )

    actions = ['activate_users', 'deactivate_users']
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"


admin.site.register(User, CustomUserAdmin)
