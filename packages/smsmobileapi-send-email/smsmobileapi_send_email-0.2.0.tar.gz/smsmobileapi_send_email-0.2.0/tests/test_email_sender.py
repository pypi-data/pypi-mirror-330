from smsmobileapi_send_email import SMSMobileAPIEmailSender

apikey = "your_account_api_key"
apikeybox = "your_email_api_key"

sender = SMSMobileAPIEmailSender(apikey, apikeybox)

response = sender.send_email(
    sender_name="John Doe",
    sender_email="john.doe@example.com",
    recipient_email="recipient@example.com",
    mail_subject="Test Email",
    mail_body="Hello, this is a test email!",
    allow_self_signed="yes"
)

print(response)
