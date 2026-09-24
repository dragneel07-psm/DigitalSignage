from django.conf import settings


def branding(request):
    return {"display_organization": settings.DISPLAY_ORGANIZATION}
