from django.contrib import admin
from .models import BlogModel, BlogCategoryModel, BlogEnModel

# Register your models here.


@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)

@admin.register(BlogEnModel)
class BlogEnAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)

@admin.register(BlogCategoryModel)
class BlogCategoryAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)