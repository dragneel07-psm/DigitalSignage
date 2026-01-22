from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notice, Device, User, AuditLog, Gallery, CitizenCharter
import inspect

# A simple way to get user without thread locals is tricky in signals.
# For this iteration, we might assume the view/serializer handles the logging or we use a library.
# However, to keep it dependency-free-ish, we will just log what changed.
# To get the USER, we generally need middleware to set it on the thread.

# Let's implement a thread local storage for user.
import threading
_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

@receiver(post_save, sender=Notice)
@receiver(post_save, sender=Device)
@receiver(post_save, sender=User)
@receiver(post_save, sender=Gallery)
@receiver(post_save, sender=CitizenCharter)
def log_save(sender, instance, created, **kwargs):
    user = get_current_user()
    action = "Created" if created else "Updated"
    model_name = sender._meta.verbose_name
    
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(instance.pk),
        details=f"{model_name} {action}: {str(instance)}"
    )

    # N8N Trigger for Published Notices (both on creation and update)
    if sender == Notice and instance.status == 'published':
        try:
            import requests
            from django.conf import settings
            if hasattr(settings, 'N8N_WEBHOOK_URL'):
                requests.post(settings.N8N_WEBHOOK_URL, json={
                    'event': 'notice_published',
                    'id': instance.id,
                    'title': instance.title,
                    'content': instance.content
                }, timeout=2)
        except Exception as e:
            print(f"Failed to trigger n8n: {e}")

@receiver(post_delete, sender=Notice)
@receiver(post_delete, sender=Device)
def log_delete(sender, instance, **kwargs):
    user = get_current_user()
    model_name = sender._meta.verbose_name
    
    AuditLog.objects.create(
        user=user,
        action="Deleted",
        model_name=model_name,
        object_id=str(instance.pk),
        details=f"{model_name} Deleted: {str(instance)}"
    )
