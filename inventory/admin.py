from django.contrib import admin
from django.db import models
from .models import (
    Category,
    Subcategory,
    Size,
    Product,
    ProductVariant,
    ProductReview,
    ProductShipping,
    ProductImage,
    ReviewImage,
    Discount,
    DiscountHistory,
    PriceHistory,
    InventoryTransaction,
    Coupon,
    ProductFaq,
    Color
)
from django.utils.html import format_html
from admin_extra_buttons.api import ExtraButtonsMixin, button
from django.http import HttpResponse
import csv
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .resources import ProductVariantResource
from .forms import ProductExportForm






# Inline admin configurations for related models
class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 1
    readonly_fields = ('stock_quantity',)
    show_change_link = True

class ProductFaqInline(admin.StackedInline):
    '''Stacked Inline View for ProductFaq'''

    model = ProductFaq
    extra = 1

class ReviewImageInline(admin.StackedInline):
    '''Stacked Inline View for ReviewImageInline'''

    model = ReviewImage
    readonly_fields = ('image',)
    extra = 1

class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ('image','is_main')
    show_change_link = True

class ProductReviewInline(admin.StackedInline):
    model = ProductReview
    extra = 1
    fields = ('user', 'rating', 'comment', 'is_verified')
    readonly_fields = fields
    show_change_link = True

class PriceHistoryInline(admin.TabularInline):
    model = PriceHistory
    extra = 1
    # fields = ('price', 'timestamp')
    readonly_fields = ('timestamp',)  # Make 'timestamp' visible but not editable
    show_change_link = True

class ProductShippingInline(admin.StackedInline):
    '''Tabular Inline View for ProductShipping'''

    model = ProductShipping
    extra = 1
    max_num = 1 


class DiscountHistoryInline(admin.TabularInline):
    model = DiscountHistory
    extra = 1
    fields = ('discount', 'usage_count', 'timestamp')
    show_change_link = True

class InventoryTransactionInline(admin.TabularInline):
    model = InventoryTransaction
    extra = 1
    fields = ('product_variant', 'quantity', 'transaction_type', 'created_at')
    show_change_link = True

# ModelAdmin Customizations with Jazzmin's features
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'slug', 'products_count')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 25
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'slug', 'description', 'thumbnail')
        }),
        ('SEO Information', {
            'fields': ('seo_meta_title', 'seo_meta_description', 'seo_meta_keywords', 'additional_seo')
        }),
    )
    
    

    def image_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.thumbnail.url)
        return "-"
    image_preview.short_description = "Thumbnail"
    



class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['category']
    list_per_page = 25
    fieldsets = (
        ('General Information', {
            'fields': ('category', 'name', 'slug', 'description')
        }),
        ('SEO Information', {
            'fields': ('seo_meta_title', 'seo_meta_description', 'seo_meta_keywords', 'additional_seo')
        }),
    )

class ProductAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ('name', 'slug', 'sku', 'category', 'subcategory', 'is_active')
    search_fields = ('name', 'sku', 'category__name', 'subcategory__name')
    list_filter = ('category__name', 'subcategory', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline, ProductReviewInline, ProductFaqInline, ProductShippingInline]
    list_per_page = 25
    fieldsets = (
        ('General Information', {
            'fields': ('name', 'slug', 'price', 'sku', 'description', 'category', 'subcategory', 'seller_pdf', 'thumbnail', 'tax', 'is_active')
        }),
        ('SEO Information', {
            'fields': ('seo_meta_title', 'seo_meta_description', 'seo_meta_keywords', 'additional_seo')
        }),
    )




class ProductVariantAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('product', 'price', 'stock_quantity', 'is_active')
    search_fields = ('sku', 'product__name', 'name')
    list_filter = ('product__name','is_active')
    list_per_page = 25
    resource_classes  = [ProductVariantResource,]
    inlines = [ProductImageInline, PriceHistoryInline]
    # action_form = SimpleActionForm
    




class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_verified', 'created_at', 'updated_at')
    search_fields = ('product__name', 'user__username', 'rating')
    list_filter = ('rating', 'is_verified', 'created_at', 'updated_at')
    list_per_page = 25
    inlines = [ReviewImageInline]

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_type', 'value', 'start_date', 'end_date', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('discount_type', 'start_date', 'end_date', 'created_at', 'updated_at')
    list_per_page = 25

class DiscountHistoryAdmin(admin.ModelAdmin):
    list_display = ('discount', 'usage_count', 'timestamp')
    search_fields = ('discount__name',)
    list_filter = ('timestamp',)
    list_per_page = 25

class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'price', 'timestamp')
    search_fields = ('product_variant__name',)
    list_filter = ('timestamp',)
    list_per_page = 25

class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'quantity', 'transaction_type', 'created_at')
    search_fields = ('product_variant__name',)
    list_filter = ('transaction_type', 'created_at')
    list_per_page = 25

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'is_active', 'created_at')
    search_fields = ('code',)
    list_filter = ('is_active', 'created_at')
    list_per_page = 25
    fieldsets = (
        ('General Information', {
            'fields': ('code', 'discount_type', 'value', 'scope', 'category', 'product', 'is_active',)
        }),
        ('Usage Information', {
            'fields': ('usage_limit', 'usage_count')
        }),
      
    )

# Register models to the admin interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
# admin.site.register(ProductShipping)
# admin.site.register(ProductImage)
# admin.site.register(ReviewImage)
admin.site.register(Discount, DiscountAdmin)
# admin.site.register(DiscountHistory, DiscountHistoryAdmin)
admin.site.register(Color)
admin.site.register(InventoryTransaction, InventoryTransactionAdmin)
admin.site.register(Coupon, CouponAdmin)



