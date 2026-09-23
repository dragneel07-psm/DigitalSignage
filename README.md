# DigitalSignage — डिजिटल सूचना पाटी

[![CI](https://github.com/dragneel07-psm/DigitalSignage/actions/workflows/ci.yml/badge.svg)](https://github.com/dragneel07-psm/DigitalSignage/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A self-hosted, Django-based digital noticeboard with Nepali-language interfaces.
Manage notices, citizen charters, images, videos, and scrolling messages from a
central dashboard and show them in a browser on a TV or monitor.

## Purpose and intended users

Designed for municipalities, schools, offices, and community institutions that
need locally relevant public information displays. Citizen charters describe
services, required documents, fees, processing times, and responsible officers.
The project is available for use, modification, and redistribution under MIT.
These are intended use cases, not claims of verified deployments or adoption.

## Implemented features

- Notice publishing, priorities, expiry dates, and target-device associations.
- Full-screen browser player, image galleries, uploaded videos, and YouTube embeds.
- Citizen charters, contact information, and official representative profiles.
- Ordered scrolling messages and Nepali date support.
- Account-based dashboard, administration, and audit records.
- Django REST Framework APIs and Docker build configuration.

## Local setup

Requires Python 3.10 or later. SQLite is the configured database; Node.js is only
needed when rebuilding Tailwind CSS. Python 3.10 and 3.13 are covered by CI.

```sh
git clone https://github.com/dragneel07-psm/DigitalSignage.git
cd DigitalSignage
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

On Windows, activate with `.venv\Scripts\activate` instead.

1. Sign in at `http://127.0.0.1:8000/admin/` using the account you created.
2. Add a Device and note its ID. Add a Notice, select its target device, and set
   its status to `published`. Optionally add citizen charters, galleries, and tickers.
3. Open `http://127.0.0.1:8000/display/<device-id>/` in a browser and enter full screen.
4. The everyday management dashboard is at `http://127.0.0.1:8000/dashboard/`.

There is no default administrator password. Create and manage your own accounts.

## Docker development

```sh
docker compose up --build -d
docker compose exec web python manage.py createsuperuser
```

The included Compose file is for local development. It enables debug mode and
mounts the checkout so SQLite data survives container replacement. Do not expose
this configuration directly to the internet. Container startup runs migrations
and collects static files; it does not create users or reset their passwords.

The existing image publishing workflow builds for AMD64, ARM64, and ARMv7 and
requires the maintainer's Docker Hub credentials. An architecture appearing in
that workflow is not proof that every build has passed.

## Configuration and deployment

Environment variables are read from the process environment; `.env` files are
not loaded automatically by Django.

| Variable | Behavior |
| --- | --- |
| `DEBUG` | Defaults to `True` for local development; set `False` for production. |
| `SECRET_KEY` | Required when debug is disabled. Generate a unique secret. |
| `ALLOWED_HOSTS` | Comma-separated hostnames; defaults to localhost/loopback. |
| `CORS_ALLOWED_ORIGINS` | Optional comma-separated trusted origins; none by default. |

Before deployment, configure HTTPS, secure cookies and proxy settings in Django,
serve `/media/` through your web server or media storage, and persist/back up both
`db.sqlite3` and `media/`. WhiteNoise serves collected static assets, not uploaded
media. `DATABASE_URL` is not implemented: switching to PostgreSQL requires an
explicit Django `DATABASES` configuration. Run `python manage.py check --deploy`
with your deployment settings and resolve its warnings.

The public display and read APIs expose published notices and display content.
Only upload information intended for public display. Authentication is required
to write through APIs. This is not a multi-tenant security boundary; API write
permissions and institution-specific role policies need review before deployment.
YouTube and some frontend/date resources require internet access; offline playback
is not guaranteed. Read [SECURITY.md](SECURITY.md) before deployment.

## Development and verification

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
npm ci
npm run build:css
```

CI runs Django checks, migration drift detection, tests, and the CSS build.
Read [CONTRIBUTING.md](CONTRIBUTING.md) for the review process and
[ROADMAP.md](ROADMAP.md) for planned work. Report reproducible bugs using
[GitHub Issues](https://github.com/dragneel07-psm/DigitalSignage/issues).

## License

Copyright (c) 2026 Pramod Singh Manyal. Project code is licensed under the
[MIT License](LICENSE). Dependencies and third-party assets retain their own licenses.
