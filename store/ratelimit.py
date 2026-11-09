import hashlib
import ipaddress
from datetime import timedelta

from django.utils import timezone

from .models import ResetAttempt

WINDOW = timedelta(hours=1)
MAX_PER_EMAIL = 3
MAX_PER_IP = 10


def _hash(email):
    return hashlib.sha256(email.strip().lower().encode()).hexdigest()


def client_ip(request):
    value = request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
    value = value or request.META.get("REMOTE_ADDR", "")
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        return None


def is_limited(email, ip):
    recent = ResetAttempt.objects.filter(created__gte=timezone.now() - WINDOW)
    if recent.filter(email_hash=_hash(email)).count() >= MAX_PER_EMAIL:
        return True
    if ip and recent.filter(ip=ip).count() >= MAX_PER_IP:
        return True
    return False


def record_attempt(email, ip):
    ResetAttempt.objects.filter(created__lt=timezone.now() - WINDOW).delete()
    ResetAttempt.objects.create(email_hash=_hash(email), ip=ip)