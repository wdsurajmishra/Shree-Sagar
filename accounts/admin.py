from django.contrib import admin
from django.http import HttpRequest
from .models import Roles, Staff, Customer, WalletHistory, Wallet, WishList
from import_export.admin import ExportActionMixin
from import_export.admin import ExportMixin

# Register your models here.
@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')
        }),
        ('Contact Details', {
            'fields': ('phone',),
        }),
        ('Profile', {
            'fields': ('profile_picture',),
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'role', 'user_permissions'),
        }),
        ('OTP Information', {
            'fields': ('otp', 'otp_created_at'),
            'description': 'Fields for OTP generation and validation.',
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    exclude = ('is_superuser',)
    readonly_fields = ('otp', 'otp_created_at')
    list_display = ('username', 'email', 'phone', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')
        }),
        ('Contact Details', {
            'fields': ('phone',),
        }),
        ('Profile', {
            'fields': ('profile_picture',),
        }),
        ('OTP Information', {
            'fields': ('otp', 'otp_created_at'),
            'description': 'Fields for OTP generation and validation.',
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    exclude = ('is_superuser',)
    readonly_fields = ('otp', 'otp_created_at')
    list_display = ('username', 'first_name', 'email', 'phone', 'ban')
    list_filter = ('ban',)
    search_fields = ('username', 'email', 'phone')
    
class WalletHistoryInline(admin.StackedInline):
    '''Stacked Inline View for WalletHistory'''

    model = WalletHistory
    fields = ('amount', 'note', 'created_at')
    readonly_fields = fields
    extra = 1
    

class WalletAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username', 'user__email', 'user__phone')
    inlines = [WalletHistoryInline]


@admin.register(WishList)
class WishListAdmin(ExportActionMixin,admin.ModelAdmin):
    list_display = ('user', 'product')
    search_fields = ('user__username', 'user__email', 'user__phone', 'product__name')
    list_filter = ('product__category', 'created_at')


    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

admin.site.register(Wallet, WalletAdmin)        