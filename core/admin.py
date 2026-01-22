from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, Notice, Contact, Device, Gallery, Photo, CitizenCharter, AuditLog
)

# Register your models here.
admin.site.register(User, UserAdmin)

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'location_description', 'is_active', 'last_seen')
    list_filter = ('is_active',)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'published_date')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'content')

class PhotoInline(admin.TabularInline):
    model = Photo

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [PhotoInline]
    list_display = ('title', 'created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'duration')
        }),
        ('Media', {
            'fields': ('cover_image', 'youtube_url'),
            'description': 'Upload a local file OR enter a YouTube URL (not both)'
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'created_by')

@admin.register(CitizenCharter)
class CitizenCharterAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'service_time', 'service_fee', 'responsible_officer')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model_name', 'ip_address')
    readonly_fields = ('timestamp', 'user', 'action', 'model_name', 'object_id', 'details', 'ip_address')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'position')
    search_fields = ('full_name', 'phone_number', 'position')
