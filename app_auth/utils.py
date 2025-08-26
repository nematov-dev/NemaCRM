# utils.py
import random
from django.core.mail import send_mail
from django.conf import settings

def send_verification_code(email):
    code = random.randint(100000, 999999)  # 6 xonali kod
    subject = "Tasdiqlash kodi"
    message = f"Sizning tasdiqlash kodingiz: {code}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
    return code
