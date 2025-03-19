from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings

class EmailService:
    """Service to send emails using Django's configured email backend."""

    @staticmethod
    def send_email(subject, message, recipient_list, from_email=None):
        """
        Sends an email using Django's email backend.
        
        :param subject: Email subject
        :param message: Email body
        :param recipient_list: List of recipients (['user@example.com'])
        :param from_email: Sender email (default: settings.DEFAULT_FROM_EMAIL)
        :return: Number of successfully delivered messages
        """
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        return send_mail(subject, message, from_email, recipient_list)
    

    @staticmethod
    def send_html_email(subject, message, recipient_list, from_email=None, html_message=None):
        """
        Sends an email with optional HTML formatting.

        :param subject: Email subject
        :param message: Plain text fallback for email
        :param recipient_list: List of recipients (['customer@example.com'])
        :param from_email: Sender email (default: settings.DEFAULT_FROM_EMAIL)
        :param html_message: HTML version of the email
        :return: Number of successfully delivered messages
        """
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL

        email = EmailMultiAlternatives(subject, message, from_email, recipient_list)
        if html_message:
            email.attach_alternative(html_message, "text/html")
        return email.send()