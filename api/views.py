from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from rest_framework import status
from rest_framework.response import Response
from django.template import Context
from email.mime.image import MIMEImage
from django.template.loader import get_template
from booksapp.settings import EMAIL_HOST_USER as email_host
from django.contrib.staticfiles import finders
from functools import lru_cache
from django.shortcuts import render


@lru_cache()
def image_data():
    with open(finders.find('image.png'), 'rb') as f:
        image_data = f.read()
    image = MIMEImage(image_data)
    image.add_header('Content-ID', '<image>')
    return image

class home(APIView):
    def get(self, request):
        body = {
            'username':"aksh",
            'send_to':'akshsharma1218@gmail.com'
        }
        return Response({"request_body":body}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        send_to = request.data['send_to']
        print(send_to)
        message = get_template("template.html").render({'username': request.data['username']})
        mail = EmailMultiAlternatives(
            subject="Welcome to Sravni.ru",
            body=message,
            from_email=email_host,
            to=[send_to],
            **kwargs
        )
        mail.content_subtype = "html"
        mail.mixed_subtype = 'related'
        mail.attach_alternative(message, "text/html")
        mail.attach(image_data())
        mail.send(fail_silently=False)
        return Response({"success": "Sent"}, status=status.HTTP_200_OK)