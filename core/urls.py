from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from . import admin_views

router = DefaultRouter()
# router.register(r'offices', views.OfficeViewSet)
router.register(r'devices', views.DeviceViewSet)
router.register(r'notices', views.NoticeViewSet)
router.register(r'galleries', views.GalleryViewSet)
router.register(r'charters', views.CitizenCharterViewSet)
router.register(r'ticker', views.TickerViewSet)

from django.views.generic import RedirectView

urlpatterns = [
    # Redirect root to dashboard
    path('', RedirectView.as_view(pattern_name='dashboard')),
    

    # Admin Panel Views
    path('dashboard/', admin_views.DashboardView.as_view(), name='dashboard'),
    
    # Placeholder for other admin views
    path('notices/list/', admin_views.NoticeListView.as_view(), name='notice_list'),
    path('notices/create/', admin_views.NoticeCreateView.as_view(), name='notice_create'),
    path('notices/<int:pk>/edit/', admin_views.NoticeUpdateView.as_view(), name='notice_edit'),
    path('notices/<int:pk>/delete/', admin_views.NoticeDeleteView.as_view(), name='notice_delete'),
    path('devices/list/', admin_views.DeviceListView.as_view(), name='device_list'),
    path('devices/create/', admin_views.DeviceCreateView.as_view(), name='device_create'),
    path('display/<int:device_id>/', admin_views.PlayerView.as_view(), name='player_display'),
    
    # Gallery & Charter
    path('gallery/list/', admin_views.GalleryListView.as_view(), name='gallery_list'),
    path('gallery/create/', admin_views.GalleryCreateView.as_view(), name='gallery_create'),
    path('gallery/<int:pk>/edit/', admin_views.GalleryUpdateView.as_view(), name='gallery_edit'),
    path('gallery/<int:pk>/delete/', admin_views.GalleryDeleteView.as_view(), name='gallery_delete'),
    path('charter/list/', admin_views.CitizenCharterListView.as_view(), name='charter_list'),
    path('charter/create/', admin_views.CitizenCharterCreateView.as_view(), name='charter_create'),
    path('charter/<int:pk>/edit/', admin_views.CitizenCharterUpdateView.as_view(), name='charter_edit'),
    path('charter/<int:pk>/delete/', admin_views.CitizenCharterDeleteView.as_view(), name='charter_delete'),

    # Ticker Management
    path('tickers/list/', admin_views.TickerListView.as_view(), name='ticker_list'),
    path('tickers/create/', admin_views.TickerCreateView.as_view(), name='ticker_create'),
    path('tickers/<int:pk>/edit/', admin_views.TickerUpdateView.as_view(), name='ticker_edit'),
    path('tickers/<int:pk>/delete/', admin_views.TickerDeleteView.as_view(), name='ticker_delete'),

    # User Management
    path('users/list/', admin_views.UserListView.as_view(), name='user_list'),
    path('users/create/', admin_views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/edit/', admin_views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/password/', admin_views.UserPasswordChangeView.as_view(), name='user_password_change'),
    path('users/<int:pk>/delete/', admin_views.UserDeleteView.as_view(), name='user_delete'),
    
    # Contact Management
    path('contacts/list/', admin_views.ContactListView.as_view(), name='contact_list'),
    path('contacts/create/', admin_views.ContactCreateView.as_view(), name='contact_create'),
    path('contacts/<int:pk>/edit/', admin_views.ContactUpdateView.as_view(), name='contact_edit'),
    path('contacts/<int:pk>/delete/', admin_views.ContactDeleteView.as_view(), name='contact_delete'),
    
    path('password-change/', admin_views.MyPasswordChangeView.as_view(), name='my_password_change'),
    path('settings/', admin_views.SettingsView.as_view(), name='settings'),


    # API endpoints
    path('api/v1/', include(router.urls)),
    path('api/v1/nepali-date/', views.get_nepali_date, name='nepali_date'),
    path('api/v1/auth/login/', obtain_auth_token, name='api_token_auth'),
    # Action Request Management
    path('requests/list/', admin_views.ActionRequestListView.as_view(), name='action_request_list'),
    path('requests/create/<str:model_name>/<int:object_id>/<str:request_type>/', 
         admin_views.ActionRequestCreateView.as_view(), name='action_request_create'),
    path('requests/<int:pk>/delete/', admin_views.ActionRequestDeleteView.as_view(), name='action_request_delete'),

    path('reports/', admin_views.ReportView.as_view(), name='system_report'),
]
