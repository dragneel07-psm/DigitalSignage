"""Create fictional display content in the explicitly isolated demo environment."""
from datetime import timedelta
from io import BytesIO
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from PIL import Image, ImageDraw
from core.models import CitizenCharter, Device, Gallery, Notice, Representative, TickerMessage


class Command(BaseCommand):
    help = "Seed fictional content; requires DigitalSignage.demo_settings. Creates no user accounts."

    @transaction.atomic
    def handle(self, *args, **options):
        if not getattr(settings, "DEMO_MODE", False):
            raise CommandError("Use --settings=DigitalSignage.demo_settings to keep demo data separate.")
        device, _ = Device.objects.get_or_create(
            name="DEMO — Community screen", defaults={"location_description": "Fictional community centre"})
        for title, content in [
            ("नमुना सूचना · सामुदायिक पुस्तकालय", "यो प्रदर्शनका लागि बनाइएको काल्पनिक सूचना हो। पुस्तकालय परिचय कार्यक्रम बिहान १० बजे।"),
            ("DEMO · Digital skills workshop", "Fictional event: learn to publish notices and manage a community screen. No registration required."),
            ("नमुना सूचना · सरसफाइ कार्यक्रम", "नमुना समुदायमा सरसफाइ कार्यक्रम। यो वास्तविक कार्यक्रमको सूचना होइन।"),
        ]:
            notice, _ = Notice.objects.get_or_create(title=title, defaults={
                "content": content, "status": "published", "published_date": timezone.now(),
                "expiry_date": timezone.localdate() + timedelta(days=30)})
            notice.target_devices.add(device)
        CitizenCharter.objects.get_or_create(service_name="नमुना सेवा · पुस्तकालय सदस्यता", defaults={
            "required_docs": "नमुना परिचयपत्र (प्रदर्शन मात्र)", "service_time": "१० मिनेट (नमुना)",
            "service_fee": "निःशुल्क (नमुना)", "responsible_officer": "नमुना सेवा कक्ष"})
        TickerMessage.objects.get_or_create(content="DEMO ONLY · सबै सामग्री काल्पनिक हुन् · Help improve Nepali community information displays", defaults={"order": 0})
        Representative.objects.get_or_create(full_name="नमुना प्रतिनिधि · Demo contact", defaults={
            "designation": "अन्य", "custom_designation": "काल्पनिक सहायता कक्ष", "email": "demo@example.org"})
        gallery, created = Gallery.objects.get_or_create(title="DEMO — Community learning", defaults={"duration": 10})
        if created:
            picture = Image.new("RGB", (1200, 675), "#123751")
            draw = ImageDraw.Draw(picture)
            draw.text((75, 160), "COMMUNITY LEARNING", fill="white", font_size=64)
            draw.text((75, 290), "Share notices. Explain services.", fill="#c4e5dc", font_size=40)
            draw.text((75, 355), "Welcome your community.", fill="#c4e5dc", font_size=40)
            draw.text((75, 560), "FICTIONAL DEMO CONTENT", fill="white", font_size=26)
            output = BytesIO()
            picture.save(output, format="PNG")
            gallery.cover_image.save("demo-community.png", ContentFile(output.getvalue()), save=True)
        self.stdout.write(self.style.SUCCESS(f"Demo ready: http://127.0.0.1:8000/display/{device.pk}/"))
        self.stdout.write("Fictional records only. No user accounts were created. Reruns preserve existing demo records.")
