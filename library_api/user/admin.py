from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserLibraryRelation


class UserLibraryRelationInline(admin.TabularInline):
    model = UserLibraryRelation
    extra = 1  # Number of extra forms to display


class CustomUserAdmin(UserAdmin):
    inlines = [UserLibraryRelationInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # ('Library Admin Info', {'fields': ('is_library_admin',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
