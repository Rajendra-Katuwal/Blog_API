from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.urls import reverse

def send_email_verification_mail(request, user):
    refresh = RefreshToken.for_user(user)
    refresh.access_token.set_exp(lifetime=timedelta(minutes=60))  # 1 Hour
    token = str(refresh.access_token)

    domain = get_current_site(request).domain
    verification_link = f"http://{domain}/api/user/verify-email/?token={token}"

    subject = "Verify your email address"
    body = render_to_string(
        "emails/verification_email.html",
        {
            "verification_link": verification_link,
        },
    )

    email = EmailMessage(subject, body, from_email="noreply@journalify.com", to=[user.email])
    email.content_subtype = "html"  # Set the content type to HTML
    email.send()

