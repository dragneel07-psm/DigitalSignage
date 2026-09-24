# Try DigitalSignage with fictional content

This local demo uses **demo.sqlite3** and **demo-media/**, separate from the normal
application database and uploads. Every notice and contact is fictional. Do not
use this development configuration as an internet-facing service.

## Start the display

After the README's clone, virtual environment, and dependency installation steps:

```sh
python manage.py migrate --settings=DigitalSignage.demo_settings
python manage.py seed_demo --settings=DigitalSignage.demo_settings
python manage.py runserver 127.0.0.1:8000 --settings=DigitalSignage.demo_settings
```

Open the display URL printed by `seed_demo`. The seed command creates sample
notices, a citizen charter, a ticker, a fictional contact, and a media card. It
creates no accounts, never resets passwords, and refuses to run with the normal
settings. Rerunning it preserves existing demo content rather than duplicating it.

## Try editing

In another activated terminal, create your own local administrator:

```sh
python manage.py createsuperuser --settings=DigitalSignage.demo_settings
```

Sign in at `/dashboard/` or `/admin/`. Open the Notices page, create a notice,
select the demo device, and set the status to Published. Reopen the display to
see your notice. Demo data expires after 30 days; edit expiry dates if you keep
using the same demo database.

## Your organization

For a normal installation, export `DISPLAY_ORGANIZATION` before starting Django
to override the display's original municipality heading. The isolated demo sets
a fictional heading automatically. Other institution-specific text and branding
may still need customization; the demo is not an endorsement by any institution.

## Give useful feedback

Use [Q&A](https://github.com/dragneel07-psm/DigitalSignage/discussions/categories/q-a)
for setup help. Include your operating system, Python version, and the step that
failed. In public feedback, use synthetic content and remove credentials.

For [Show and tell](https://github.com/dragneel07-psm/DigitalSignage/discussions/categories/show-and-tell),
share your intended use, screen/browser, what worked, and one improvement you need.
Only identify an institution or share screenshots if you have permission.
