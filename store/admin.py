from django.contrib import admin
from .models import *
import os

# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImageModel
    # readonly_fields = ("user",)


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(DesignPatternModel)
class DesignPatternAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")

    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
    
    
@admin.register(TagsModel)
class TagsAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(WateModel)
class WateAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(TextureModel)
class TextureAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
    

@admin.register(PileModel)
class PileAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    readonly_fields = ("user", "created_date", "modified_date", "visit")
    search_fields = ('code',)
    list_display = ["code", "price", "price_in", "available"]
    list_filter = ["available", "on_sale"]
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(ProductImageModel)
class ProductImageAdmin(admin.ModelAdmin):
    readonly_fields = ("created_date",)
    search_fields = ('name__code',)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)