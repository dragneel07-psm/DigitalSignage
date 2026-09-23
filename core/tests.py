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



class PublicNoticeTest(TestCase):
    def setUp(self):
        from datetime import timedelta
        from django.utils import timezone
        self.today = timezone.localdate()
        self.user = User.objects.create_user(username='editor', password='test-only')
        self.visible = Notice.objects.create(title='Public', content='Public text', status='published')
        self.today_notice = Notice.objects.create(
            title='Expires today', content='Still public', status='published', expiry_date=self.today)
        self.draft = Notice.objects.create(title='Draft', content='Private draft', status='draft')
        self.expired = Notice.objects.create(
            title='Expired', content='Old', status='published', expiry_date=self.today - timedelta(days=1))

    def test_anonymous_lists_only_current_published_notices(self):
        for url in ['/api/v1/notices/', '/api/v1/notices/published/']:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual({item['id'] for item in response.json()},
                                 {self.visible.pk, self.today_notice.pk})

    def test_anonymous_cannot_retrieve_draft_or_expired_notice(self):
        for notice in [self.draft, self.expired]:
            self.assertEqual(self.client.get(f'/api/v1/notices/{notice.pk}/').status_code, 404)
        self.assertEqual(self.client.get(f'/api/v1/notices/{self.visible.pk}/').status_code, 200)

    def test_authenticated_editor_can_read_drafts(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(f'/api/v1/notices/{self.draft.pk}/').status_code, 200)
        response = self.client.get('/api/v1/notices/published/')
        self.assertNotIn(self.draft.pk, {item['id'] for item in response.json()})

    def test_anonymous_cannot_create_notice(self):
        response = self.client.post('/api/v1/notices/', {'title': 'Bad', 'content': 'Not allowed'})
        self.assertIn(response.status_code, [401, 403])
        self.assertFalse(Notice.objects.filter(title='Bad').exists())


class DeploymentConfigurationTest(TestCase):
    def test_production_requires_secret(self):
        import os
        import subprocess
        import sys
        env = {k: v for k, v in os.environ.items() if k != 'SECRET_KEY'}
        env['DEBUG'] = 'False'
        result = subprocess.run([sys.executable, '-c', 'import DigitalSignage.settings'],
                                env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Set SECRET_KEY when DEBUG=False', result.stderr)
        env['SECRET_KEY'] = 'test-only-configuration-key'
        result = subprocess.run([sys.executable, '-c', 'import DigitalSignage.settings'],
                                env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_container_startup_preserves_accounts(self):
        import os
        from pathlib import Path
        import subprocess
        import tempfile
        from django.conf import settings
        # A command recorder verifies startup invokes only migrations, static
        # collection, and the requested server; no account mutation command.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            recorder = root / 'python'
            recorder.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$STARTUP_LOG"\n')
            recorder.chmod(0o755)
            log = root / 'commands'
            env = dict(os.environ, PATH=f'{root}:' + os.environ.get('PATH', ''), STARTUP_LOG=str(log))
            result = subprocess.run(['sh', str(settings.BASE_DIR / 'entrypoint.sh'),
                                     'python', 'server-sentinel'], env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(log.read_text().splitlines(),
                             ['manage.py migrate', 'manage.py collectstatic --noinput', 'server-sentinel'])
