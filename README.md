# Digital Signage System

A modern, responsive Digital Signage system built with Django. This system allows for central management of content (notices, images, and YouTube videos) to be displayed on remote screens.

![Project Preview](https://via.placeholder.com/1200x600?text=Digital+Signage+System+Preview)

## Features

- **Centralized Dashboard**: Manage all signage content from a single admin interface.
- **Dynamic Playlists**: Support for images and YouTube videos with configurable durations.
- **Real-time Notices**: Display scrolling or static text notices across the bottom of the screen.
- **YouTube Integration**: Seamlessly embed YouTube videos (Note: Use "Mute" by default for autoplay compatibility).
- **Responsive Player**: A dedicated player view designed for full-screen display on TVs and monitors.
- **Audit Logs**: Track sensitive actions within the admin panel.

## Tech Stack

- **Backend**: Python 3.10+, Django 5.x
- **Frontend**: Vanilla CSS, JavaScript, Tailwind CSS (for admin/dashboard components)
- **Database**: SQLite (default), PostgreSQL (supported)
- **Deployment**: Docker, Gunicorn, WhiteNoise

## Quick Start (Local Development)

### Prerequisites
- Python 3.10 or higher
- [Optional] Docker and Docker Compose

### Manual Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/DigitalSignage.git
   cd DigitalSignage
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server**:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/admin` to login and `http://127.0.0.1:8000/display/1/` to view the signage.

### Docker Setup (Using Docker Hub Image)

**Quick Start**: Pull and run the pre-built image from Docker Hub:

1. **Pull the image**:
   ```bash
   docker pull dragneel07/digital-signage:latest
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 \
     -e DEBUG=False \
     -e SECRET_KEY=your-secret-key-here \
     -e ALLOWED_HOSTS=* \
     --name digital-signage \
     dragneel07/digital-signage:latest
   ```
   The application will be available at `http://localhost:8000`.

### Docker Setup (Build from Source)
1. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```
   The application will be available at `http://localhost:8000`.

### CI/CD - Automated Builds

This repository includes a GitHub Actions workflow to automatically build and push multi-architecture Docker images (amd64/arm64) to Docker Hub.

#### Setup Instructions

To enable automated builds:

1. Go to your repository **Settings** > **Secrets and variables** > **Actions**
2. Add the following repository secrets:
    * `DOCKER_USERNAME`: Your Docker Hub username
    * `DOCKER_PASSWORD`: Your Docker Hub password or access token

The workflow runs automatically on every push to the `master` branch.

## Deployment Instructions

### Environment Variables
Configure these in your hosting environment:
- `DEBUG`: Set to `False` in production.
- `SECRET_KEY`: A long, random string.
- `ALLOWED_HOSTS`: Comma-separated list of allowed domains (e.g., `yourdomain.com,www.yourdomain.com`).
- `DATABASE_URL`: [Optional] If using an external database.

### Hosting on Render/Railway
1. Connect your GitHub repository.
2. Set the build command to: `pip install -r requirements.txt`.
3. Set the start command to: `gunicorn DigitalSignage.wsgi:application --bind 0.0.0.0:$PORT`.
4. Ensure the environment variables above are set.

### Hosting on a VPS (Docker)
1. Install Docker and Docker Compose on your VPS.
2. Clone the repo and run `docker-compose up -d`.
3. Use a reverse proxy like Nginx or Caddy to handle SSL (HTTPS).

## License

This project is open-source. See the [LICENSE](LICENSE) file for details (if applicable).

---
Developed with ❤️ for Advanced Signage Solutions.
