from celery import shared_task
from django.utils import timezone
from .models import Cart

@shared_task
def delete_empty_guest_carts():
    three_days_ago = timezone.now() - timezone.timedelta(days=3)
    empty_guest_carts = Cart.objects.filter(user__isnull=True, created_at__lt=three_days_ago)
    empty_guest_carts.delete()
