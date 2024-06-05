import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import url_for
from app.models import User

def send_reset_email(user):
    token = user.get_reset_token()
    reset_url = url_for('auth.reset_password', token=token, _external=True)
    email_content = f"""
    <h1>Password Reset Request</h1>
    <p>To reset your password, visit the following link:</p>
    <p><a href="{reset_url}">Reset Password</a></p>
    <p>If you did not make this request, simply ignore this email and no changes will be made.</p>
    """
    
    # Configure the Sendinblue API client
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv('SENDINBLUE_API_KEY')

    # Create an instance of the API client
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

    # Define the email parameters
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": user.email}],
        subject="Password Reset Request",
        html_content=email_content,
        sender={"email": "noreply@demo.com", "name": "Demo App"}
    )

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email sent: %s" % api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
