"""Isolated local demo; never point this configuration at a production database."""
from .settings import *  # noqa: F403

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "demo.sqlite3"}}
MEDIA_ROOT = BASE_DIR / "demo-media"
DISPLAY_ORGANIZATION = "नमुना समुदाय केन्द्र · DEMO"
DEMO_MODE = True
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "testserver"]
