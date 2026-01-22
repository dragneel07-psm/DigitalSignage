from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Notice, Contact

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role', 'first_name', 'last_name')
        widgets = {
            'role': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'username': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'role', 'first_name', 'last_name', 'is_active')
        widgets = {
            'role': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'username': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded text-indigo-600 focus:ring-indigo-500'}),
        }

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'priority', 'target_devices', 'status', 'published_date', 'expiry_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'content': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'status': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'published_date': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border', 'type': 'datetime-local'}),
            'expiry_date': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border', 'type': 'date'}),
            'target_devices': forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
        }

class SettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['theme_mode', 'font_size']
        widgets = {
            'theme_mode': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'font_size': forms.Select(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'phone_number', 'position']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
            'position': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500 p-2 border'}),
        }
