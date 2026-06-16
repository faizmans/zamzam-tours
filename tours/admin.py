# tours/admin.py
from django.contrib import admin
from .models import Category, TourPackage, CustomerInquiry, PackageImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# 1. Define the Inline FIRST
class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1 # Shows one blank upload row by default

# 2. Then use it in the TourPackageAdmin SECOND
@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'duration_days', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'hotel_details')
    list_editable = ('is_active', 'price')
    inlines = [PackageImageInline] # Now it knows what this is!

@admin.register(CustomerInquiry)
class CustomerInquiryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'phone_number', 'package', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'package__category')
    search_fields = ('customer_name', 'phone_number', 'email', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('status',)