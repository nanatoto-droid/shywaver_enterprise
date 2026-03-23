from django.contrib import admin
from .models import *

@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'category', 'rating', 'review_count', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'owner__username', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'created_at', 'is_published', 'views']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'featured']
    list_filter = ['category', 'is_available', 'featured']
    search_fields = ['name', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']

@admin.register(FounderTableReservation)
class FounderTableReservationAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'date', 'time', 'is_confirmed']

@admin.register(PitchWallPost)
class PitchWallPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_active', 'created_at']

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']

@admin.register(BusinessReview)
class BusinessReviewAdmin(admin.ModelAdmin):
    list_display = ['business', 'user', 'rating', 'created_at']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'business_name']

@admin.register(WaverBusinessPass)
class WaverBusinessPassAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_active', 'started_at', 'expires_at']