from smsmobileapi_send_email import SMSMobileAPIEmailSender

apikey = "9e5b417fb687ac20c80c631f0c8d457c072da4a8bf16fbed"
apikeybox = "e89606ab468ad76079787a27effa441c5b48a43e6eacbc4fbe275307a45229da"

sender = SMSMobileAPIEmailSender(apikey, apikeybox)

response = sender.send_email(

    recipient_email="info@ebernimont.be",
    mail_subject="Test Email",
    mail_body="Hello, this is a test email!",
    allow_self_signed="yes", 
    reply_email = "info@smsmobileapi.com"
)

print(response)