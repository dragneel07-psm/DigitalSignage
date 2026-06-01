from rest_framework import serializers
from .models import User, Device, Notice, Gallery, Photo, CitizenCharter, TickerMessage, Representative

class TickerMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TickerMessage
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'email')

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'caption']

class GallerySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, read_only=True)
    class Meta:
        model = Gallery
        fields = ['id', 'title', 'description', 'cover_image', 'youtube_url', 'duration', 'created_at', 'photos']

class CitizenCharterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CitizenCharter
        fields = '__all__'


class RepresentativeSerializer(serializers.ModelSerializer):
    display_designation = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Representative
        fields = ['id', 'full_name', 'designation', 'display_designation', 'phone_number', 'email', 'photo', 'photo_url', 'order']

    def get_display_designation(self, obj):
        return obj.get_display_designation()

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None
