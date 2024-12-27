from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(ExibitionModel)
class ExibitionAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date", "pk")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)


@admin.register(ContactUsModel)
class ContactUsAdmin(admin.ModelAdmin):
    readonly_fields = ("created_date",)
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
        
        
@admin.register(VideoModel)
class VideoAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
        
        
@admin.register(CustomerVideoModel)
class CustomerVideoAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
        
        
@admin.register(PosterModel)
class PosterAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
        
        
@admin.register(OnSalePosterModel)
class OnSalePosterAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
        
        
@admin.register(CityModel)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
    

@admin.register(QuestionModel)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ("user", "created_date", "modified_date")
    
    def save_model(self, request, obj, form, change):
        obj.user = request.user   
        return super().save_model(request, obj, form, change)
    

@admin.register(FooterNewsModel)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ("text", "created_date")