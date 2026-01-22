from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import User, Device, Notice, Gallery, CitizenCharter, TickerMessage
from .serializers import (UserSerializer, DeviceSerializer, 
                          NoticeSerializer, GallerySerializer, CitizenCharterSerializer, TickerMessageSerializer)

class TickerViewSet(viewsets.ModelViewSet):
    queryset = TickerMessage.objects.filter(is_active=True).order_by('order', '-created_at')
    serializer_class = TickerMessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def heartbeat(self, request, pk=None):
        device = self.get_object()
        device.last_seen = timezone.now()
        device.save()
        return Response({'status': 'active'})

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def published(self, request):
        """Public endpoint for players to get published notices"""
        today = timezone.now().date()
        from django.db.models import Q
        notices = Notice.objects.filter(
            Q(status='published') & 
            (Q(expiry_date__isnull=True) | Q(expiry_date__gte=today))
        ).order_by('-published_date')
        serializer = self.get_serializer(notices, many=True)
        return Response(serializer.data)

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

from rest_framework.views import APIView

# ... existing code ...
class CitizenCharterViewSet(viewsets.ModelViewSet):
    queryset = CitizenCharter.objects.all()
    serializer_class = CitizenCharterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# Import Nepali date function
from .nepali_date_api import get_nepali_date
