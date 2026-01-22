from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
import uuid

# User model is already defined in existing file, we will append to it or rewrite the file.
# Since rewrite is cleaner, I will rewrite the whole file with imports.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'प्रणाली प्रशासक (System Admin)'),
        ('user', 'प्रयोगकर्ता (User)'),
    )
    theme_mode = models.CharField(
        max_length=10, 
        choices=[('light', 'Light'), ('dark', 'Dark')], 
        default='light', 
        verbose_name="Theme Mode"
    )
    font_size = models.CharField(
        max_length=10, 
        choices=[('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')], 
        default='medium', 
        verbose_name="Font Size"
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="फोन नं.")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name="भूमिका")

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = "प्रयोगकर्ता"
        verbose_name_plural = "प्रयोगकर्ताहरू"


class Device(models.Model):
    name = models.CharField(max_length=100, verbose_name="यन्त्रको नाम")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP ठेगाना")
    location_description = models.CharField(max_length=200, verbose_name="राखेको स्थान")
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय")
    last_seen = models.DateTimeField(null=True, blank=True, verbose_name="अन्तिम पटक देखिएको")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "डिजिटल सूचना पाटी"
        verbose_name_plural = "डिजिटल सूचना पाटीहरू"


class Notice(models.Model):
    PRIORITY_CHOICES = (
        ('normal', 'सामान्य (Normal)'),
        ('high', 'उच्च (High)'),
        ('emergency', 'आपतकालीन (Emergency)'),
    )
    STATUS_CHOICES = (
        ('draft', 'मस्यौदा (Draft)'),
        ('recommended', 'सिफारिस गरिएको (Recommended)'),
        ('approved', 'स्वीकृत (Approved)'),
        ('published', 'प्रकाशन गरिएको (Published)'),
    )

    title = models.CharField(max_length=255, verbose_name="सूचनाको शीर्षक")
    content = models.TextField(verbose_name="सूचनाको विवरण")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal', verbose_name="प्राथमिकता")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="स्थिति")
    
    target_devices = models.ManyToManyField(Device, verbose_name="प्रकाशन हुने पाटीहरू")
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_notices', verbose_name="सिर्जनाकर्ता")
    recommended_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='recommended_notices', verbose_name="सिफारिस गर्ने")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='approved_notices', verbose_name="स्वीकृत गर्ने")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True, blank=True, verbose_name="प्रकाशन मिति")
    expiry_date = models.DateField(null=True, blank=True, verbose_name="समाप्ति मिति")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "सूचना"
        verbose_name_plural = "सूचनाहरू"


class Gallery(models.Model):
    title = models.CharField(max_length=200, verbose_name="एल्बमको नाम")
    description = models.TextField(blank=True, verbose_name="विवरण")
    cover_image = models.FileField(
        upload_to='gallery/covers/', 
        blank=True, 
        null=True, 
        verbose_name="कभर फोटो / भिडियो",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'webm', 'ogg'])]
    )
    youtube_url = models.URLField(blank=True, null=True, verbose_name="YouTube URL", help_text="YouTube video URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
    duration = models.PositiveIntegerField(default=10, verbose_name="देखाउने समय (सेकेन्डमा)", help_text="कति सेकेन्ड सम्म देखाउने? (Duration in seconds)")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="सिर्जनाकर्ता")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "फोटो ग्यालरी"
        verbose_name_plural = "फोटो ग्यालरी"


class Photo(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/', verbose_name="फोटो")
    caption = models.CharField(max_length=200, blank=True, verbose_name="क्याप्सन")
    
    class Meta:
        verbose_name = "फोटो"


class CitizenCharter(models.Model):
    service_name = models.CharField(max_length=200, verbose_name="सेवाको नाम")
    required_docs = models.TextField(verbose_name="आवश्यक कागजात")
    service_time = models.CharField(max_length=100, verbose_name="लाग्ने समय")
    service_fee = models.CharField(max_length=100, verbose_name="सेवा शुल्क")
    responsible_officer = models.CharField(max_length=100, verbose_name="जिम्मेवार अधिकारी / शाखा")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="सिर्जनाकर्ता")

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = "नागरिक वडापत्र"
        verbose_name_plural = "नागरिक वडापत्र"


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50, null=True)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "सम्परीक्षण लग" # Audit Log
        verbose_name_plural = "सम्परीक्षण लगहरू"


class Contact(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="पूरा नाम")
    phone_number = models.CharField(max_length=15, verbose_name="फोन नं.")
    position = models.CharField(max_length=100, verbose_name="पद", blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="सिर्जनाकर्ता")

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"
    
    class Meta:
        verbose_name = "सम्पर्क"
        verbose_name_plural = "सम्पर्कहरू"



class ActionRequest(models.Model):
    REQUEST_TYPES = [
        ('edit', 'सम्पादन (Edit)'),
        ('delete', 'हटाउनुहोस् (Delete)'),
    ]
    STATUS_CHOICES = [
        ('pending', 'बाँकी (Pending)'),
        ('completed', 'पूरा भयो (Completed)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="अनुरोधकर्ता")
    model_name = models.CharField(max_length=100, verbose_name="मोडलको नाम")
    object_id = models.IntegerField(verbose_name="अब्जेक्ट ID")
    object_title = models.CharField(max_length=255, verbose_name="शीर्षक/नाम")
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES, verbose_name="अनुरोधको प्रकार")
    reason = models.TextField(verbose_name="कारण")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="स्थिति")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="सिर्जना गरिएको मिति")

    def __str__(self):
        return f"{self.user.username} - {self.get_request_type_display()} - {self.object_title}"

    class Meta:
        verbose_name = "कार्य अनुरोध"
        verbose_name_plural = "कार्य अनुरोधहरू"
        ordering = ['-created_at']


class TickerMessage(models.Model):
    content = models.TextField(verbose_name="समाचार/सूचना (Message)")
    is_active = models.BooleanField(default=True, verbose_name="सक्रिय (Active)")
    order = models.PositiveIntegerField(default=0, verbose_name="क्रम (Order)")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="सिर्जनाकर्ता")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:50]

    class Meta:
        verbose_name = "टिकर सन्देश"
        verbose_name_plural = "टिकर सन्देशहरू"
        ordering = ['order', '-created_at']

