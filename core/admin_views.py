from django.views.generic import TemplateView, ListView, FormView
import requests
from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordChangeView
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Count, Avg, Max, Sum, Subquery, OuterRef
from django.http import HttpResponse
import csv
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

from .models import Notice, Device, Gallery, CitizenCharter, User, Contact, ActionRequest, AuditLog, TickerMessage
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, NoticeForm, SettingsForm, ContactForm, DeviceForm, TickerMessageForm
)

# Ticker Views
class TickerListView(LoginRequiredMixin, ListView):
    model = TickerMessage
    template_name = "admin/ticker_list.html"
    context_object_name = "tickers"
    ordering = ['order', '-created_at']

class TickerCreateView(LoginRequiredMixin, CreateView):
    model = TickerMessage
    template_name = "admin/ticker_form.html"
    fields = ['content', 'is_active', 'order']
    success_url = reverse_lazy('ticker_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "टिकर सन्देश सफलतापूर्वक सिर्जना गरियो।")
        return super().form_valid(form)

class TickerUpdateView(LoginRequiredMixin, UpdateView):
    model = TickerMessage
    template_name = "admin/ticker_form.html"
    fields = ['content', 'is_active', 'order']
    success_url = reverse_lazy('ticker_list')

    def form_valid(self, form):
        messages.success(self.request, "टिकर सन्देश सफलतापूर्वक अद्यावधिक गरियो।")
        return super().form_valid(form)

class TickerDeleteView(LoginRequiredMixin, DeleteView):
    model = TickerMessage
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy('ticker_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "टिकर सन्देश सफलतापूर्वक हटाइयो।")
        return super().delete(request, *args, **kwargs)

class AdminRoleRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'admin' or self.request.user.is_superuser

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Admin or Superuser can edit everything
        if self.request.user.role == 'admin' or self.request.user.is_superuser:
            return True
        # Owner check
        obj = self.get_object()
        return hasattr(obj, 'created_by') and obj.created_by == self.request.user

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        context['today_notices_count'] = Notice.objects.filter(
            status='published', 
            published_date__date=today
        ).count()
        
        context['active_devices_count'] = Device.objects.filter(is_active=True).count()
        # context['total_offices'] = Office.objects.count()
        context['pending_approval_count'] = Notice.objects.filter(status='recommended').count()
        context['recent_tickers'] = TickerMessage.objects.order_by('order', '-created_at')[:8]
        context['ticker_form'] = kwargs.get('ticker_form', TickerMessageForm())
        
        if self.request.user.role == 'admin' or self.request.user.is_superuser:
            context['pending_requests_count'] = ActionRequest.objects.filter(status='pending').count()
        
        return context

    def post(self, request, *args, **kwargs):
        if not (request.user.role == 'admin' or request.user.is_superuser):
            messages.error(request, "तपाईंलाई टिकर सन्देश सुरक्षित गर्ने अनुमति छैन।")
            return redirect('dashboard')

        form = TickerMessageForm(request.POST)
        if form.is_valid():
            ticker = form.save(commit=False)
            ticker.created_by = request.user
            ticker.save()
            messages.success(request, "टिकर सन्देश सफलतापूर्वक सुरक्षित गरियो।")
            return redirect('dashboard')

        messages.error(request, "कृपया टिकर सन्देशको त्रुटिहरू सच्याउनुहोस्।")
        context = self.get_context_data(ticker_form=form)
        return self.render_to_response(context)

class NoticeListView(LoginRequiredMixin, ListView):
    model = Notice
    template_name = "admin/notice_list.html"
    context_object_name = "notices"
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.GET.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    template_name = "admin/notice_form.html"
    form_class = NoticeForm
    success_url = reverse_lazy('notice_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # Auto-set published_date if status is published and no date is set
        if form.instance.status == 'published' and not form.instance.published_date:
            from django.utils import timezone
            form.instance.published_date = timezone.now()
        
        response = super().form_valid(form)
        return response

class NoticeUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, UpdateView):
    model = Notice
    template_name = "admin/notice_form.html"
    form_class = NoticeForm
    success_url = reverse_lazy('notice_list')
    
    def form_valid(self, form):
        # Auto-set published_date if status is changed to published
        if form.instance.status == 'published' and not form.instance.published_date:
            from django.utils import timezone
            form.instance.published_date = timezone.now()
        
        response = super().form_valid(form)
        return response

class NoticeDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = Notice
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy('notice_list')

class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = "admin/device_list.html"
    context_object_name = "devices"


class DeviceCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, CreateView):
    model = Device
    template_name = "admin/device_form.html"
    form_class = DeviceForm
    success_url = reverse_lazy('device_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "नयाँ उपकरण सफलतापूर्वक थपियो।")
        return response


class PlayerView(TemplateView):
    template_name = "player/display.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_id = self.kwargs.get('device_id')
        context['device_id'] = device_id
        return context

# Gallery Views
class GalleryListView(LoginRequiredMixin, ListView):
    model = Gallery
    template_name = "admin/gallery_list.html"
    context_object_name = "galleries"

class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = Gallery
    template_name = "admin/gallery_form.html"
    fields = ['title', 'description', 'cover_image', 'youtube_url', 'duration']
    success_url = reverse_lazy('gallery_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class GalleryUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, UpdateView):
    model = Gallery
    template_name = "admin/gallery_form.html"
    fields = ['title', 'description', 'cover_image', 'youtube_url', 'duration']
    success_url = reverse_lazy('gallery_list')

class GalleryDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = Gallery
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy('gallery_list')

# Citizen Charter Views
class CitizenCharterListView(LoginRequiredMixin, ListView):
    model = CitizenCharter
    template_name = "admin/charter_list.html"
    context_object_name = "charters"

class CitizenCharterCreateView(LoginRequiredMixin, CreateView):
    model = CitizenCharter
    template_name = "admin/charter_form.html"
    fields = ['service_name', 'service_time', 'service_fee', 'responsible_officer', 'required_docs']
    success_url = reverse_lazy('charter_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class CitizenCharterUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, UpdateView):
    model = CitizenCharter
    template_name = "admin/charter_form.html"
    fields = ['service_name', 'service_time', 'service_fee', 'responsible_officer', 'required_docs']
    success_url = reverse_lazy('charter_list')

class CitizenCharterDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = CitizenCharter
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy('charter_list')

# User Views
class UserListView(LoginRequiredMixin, AdminRoleRequiredMixin, ListView):
    model = User
    template_name = "admin/user_list.html"
    context_object_name = "users"

class UserCreateView(LoginRequiredMixin, AdminRoleRequiredMixin, CreateView):
    model = User
    template_name = "admin/user_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_list')

class UserUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, UpdateView):
    model = User
    template_name = "admin/user_form.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('user_list')

class UserDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = User
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy('user_list')

class UserPasswordChangeView(LoginRequiredMixin, AdminRoleRequiredMixin, FormView):
    template_name = "admin/user_password_form.html"
    form_class = SetPasswordForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.user_obj = get_object_or_404(User, pk=self.kwargs['pk'])
        kwargs['user'] = self.user_obj
        return kwargs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_user'] = self.user_obj
        return context
        
    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"Password for {self.user_obj.username} changed successfully.")
        return redirect('user_edit', pk=self.user_obj.pk)

class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "admin/my_password_change.html"
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, "तपाईंको पासवर्ड सफलतापूर्वक परिवर्तन भयो।")
        return super().form_valid(form)



class SettingsView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "admin/settings.html"
    form_class = SettingsForm
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "सेटिङहरू सफलतापूर्वक अद्यावधिक गरियो।")
        return super().form_valid(form)

# Contact Views
class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = "admin/contact_list.html"
    context_object_name = "contacts"
    ordering = ['full_name']

class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = "admin/contact_form.html"
    form_class = ContactForm
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "सम्पर्क सफलतापूर्वक सिर्जना गरियो।")
        return super().form_valid(form)

class ContactUpdateView(LoginRequiredMixin, AdminRoleRequiredMixin, UpdateView):
    model = Contact
    template_name = "admin/contact_form.html"
    form_class = ContactForm
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        messages.success(self.request, "सम्पर्क सफलतापूर्वक अद्यावधिक गरियो।")
        return super().form_valid(form)

class ContactDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = Contact
    template_name = "admin/confirm_delete.html"
    success_url = reverse_lazy('contact_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "सम्पर्क सफलतापूर्वक हटाइयो।")
        return super().delete(request, *args, **kwargs)


# Action Request Views
class ActionRequestListView(LoginRequiredMixin, AdminRoleRequiredMixin, ListView):
    model = ActionRequest
    template_name = "admin/action_request_list.html"
    context_object_name = "requests"

class ActionRequestCreateView(LoginRequiredMixin, CreateView):
    model = ActionRequest
    template_name = "admin/action_request_form.html"
    fields = ['reason']
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get('model_name')
        object_id = self.kwargs.get('object_id')
        request_type = self.kwargs.get('request_type')
        
        # Resolve object title
        model_map = {
            'Notice': Notice,
            'Contact': Contact,
            'Gallery': Gallery,
            'CitizenCharter': CitizenCharter
        }
        model_class = model_map.get(model_name)
        if model_class:
            obj = get_object_or_404(model_class, pk=object_id)
            context['target_object'] = obj
            context['request_type_display'] = 'सम्पादन (Edit)' if request_type == 'edit' else 'हटाउनुहोस् (Delete)'
        
        return context

    def form_valid(self, form):
        model_name = self.kwargs.get('model_name')
        object_id = self.kwargs.get('object_id')
        request_type = self.kwargs.get('request_type')
        
        model_map = {
            'Notice': Notice,
            'Contact': Contact,
            'Gallery': Gallery,
            'CitizenCharter': CitizenCharter
        }
        model_class = model_map.get(model_name)
        obj = get_object_or_404(model_class, pk=object_id)
        
        form.instance.user = self.request.user
        form.instance.model_name = model_name
        form.instance.object_id = object_id
        form.instance.object_title = str(obj)
        form.instance.request_type = request_type
        
        messages.success(self.request, "तपाईंको अनुरोध व्यवस्थापकलाई पठाइएको छ।")
        return super().form_valid(form)

class ActionRequestDeleteView(LoginRequiredMixin, AdminRoleRequiredMixin, DeleteView):
    model = ActionRequest
    success_url = reverse_lazy('action_request_list')
    template_name = "admin/confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "अनुरोध सफलतापूर्वक हटाइयो।")
        return super().delete(request, *args, **kwargs)


class ReportView(LoginRequiredMixin, AdminRoleRequiredMixin, TemplateView):
    template_name = "admin/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Notice Statistics
        total_notices = Notice.objects.count()
        context['total_notices'] = total_notices
        context['published_notices'] = Notice.objects.filter(status='published').count()
        context['draft_notices'] = Notice.objects.filter(status='draft').count()
        context['expired_notices'] = Notice.objects.filter(status='expired').count()
        
        context['office_stats'] = []
        
        # Other Model Counts
        context['total_contacts'] = Contact.objects.count()
        context['total_gallery'] = Gallery.objects.count()
        context['total_charters'] = CitizenCharter.objects.count()
        context['total_devices'] = Device.objects.count()
        
        # Recent Audit Logs
        context['recent_logs'] = AuditLog.objects.all()[:50]
        
        return context
