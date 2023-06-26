from django.core.mail import EmailMessage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class SendEmail:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=os.getenv('EMAIL_FROM'),
            to=[data['to_email']]
        )
        email.send()