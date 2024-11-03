from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Send a test email to verify email settings'

    def handle(self, *args, **kwargs):
        subject = "Test Email"
        message = "This is a test email to verify email settings."
        from_email = "19arrow19@gmail.com"
        recipient_list = ["rlukianchyk@gmail.com"]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        self.stdout.write(self.style.SUCCESS("Test email sent successfully"))
