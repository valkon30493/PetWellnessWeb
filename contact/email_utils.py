import json
import requests
import msal
from django.conf import settings
from .models import EmailLog  # Import the EmailLog model


def get_access_token():
    """Fetches a Microsoft Graph API access token using OAuth2."""
    authority = f"https://login.microsoftonline.com/{settings.MICROSOFT_TENANT_ID}"
    app = msal.ConfidentialClientApplication(
        settings.MICROSOFT_CLIENT_ID, authority=authority, client_credential=settings.MICROSOFT_CLIENT_SECRET
    )

    token_result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

    if not token_result or "access_token" not in token_result:
        print("🚨 ERROR: Failed to obtain access token")
        print("🛠️ DEBUG INFO:", json.dumps(token_result, indent=4))  # Print full error details
        return None

    return token_result.get("access_token", None)


def log_email(recipient, subject, message, status):
    """Logs email attempts in the database."""
    EmailLog.objects.create(
        recipient=recipient,
        subject=subject,
        message=message,
        status=status
    )


def send_email(subject, message, recipient):
    """Sends an email using Microsoft Graph API and logs it."""
    access_token = get_access_token()
    if not access_token:
        log_email(recipient, subject, message, "Failed")
        raise Exception("Failed to obtain access token.")

    endpoint = f"https://graph.microsoft.com/v1.0/users/{settings.MICROSOFT_EMAIL_SENDER}/sendMail"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    email_data = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": message},
            "toRecipients": [{"emailAddress": {"address": recipient}}]
        }
    }

    response = requests.post(endpoint, headers=headers, json=email_data)

    if response.status_code == 202:
        log_email(recipient, subject, message, "Success")
        return "Email sent successfully!"
    else:
        log_email(recipient, subject, message, "Failed")
        raise Exception(f"Failed to send email: {response.text}")


def send_auto_reply(user_email, user_name):
    """Sends an auto-reply to the user after they submit the contact form."""
    subject = "Thank you for contacting Pet Wellness Vets!"
    message = f"""
Hi {user_name},

Thank you for reaching out to us! We have received your message and will get back to you as soon as possible.

Best regards,  
Pet Wellness Vets Team  
contact@petwellnessvets.com
"""

    return send_email(subject, message, user_email)
