from datetime import timedelta
from datetime import datetime
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


def get_activation_key_expiration_date(days: int = 2) -> datetime:
    return datetime.now() + timedelta(days=days)


def send_verify_mail(user) -> bool:
    verify_link = reverse("auth:verify", args=[user.email, user.activation_key])
    title = f"{user} confirmation link"
    message = f"""
        For {user} account verification on platform 
        {settings.DOMAIN_NAME} click on verifying ling:
        {settings.DOMAIN_NAME}{verify_link}
    """
    return send_mail(
        title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False  # on prod: True
    )
