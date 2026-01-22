from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Notice

User = get_user_model()

class DashboardTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username='admin', password='password')

    def test_dashboard_login_required(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_dashboard_access(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/dashboard.html')

class HealthCheckTest(TestCase):
    def test_homepage(self):
        # Assuming there is a homepage or login page at root
        response = self.client.get('/')
        # It might be a redirect to login or a public page
        self.assertIn(response.status_code, [200, 302])

