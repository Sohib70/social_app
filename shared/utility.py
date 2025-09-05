import re
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail

phone_regex = re.compile(r'^\+?\d{9,15}$')
email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def chech_email_or_phone_number(user_input):
    if re.fullmatch(phone_regex,user_input):
        data = 'phone'
    elif re.fullmatch(email_regex,user_input):
        data = 'email'
    else:
        data = {
            'succes': False,
            'msg': "Siz xato malumot kirityapsiz"

        }
        raise ValidationError
    return data



def send_to_mail(email, code):
    send_mail(
        subject="Tasdiqlash kodi",
        message=f"Sizning tasdiqlash kodingiz: {code}",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )