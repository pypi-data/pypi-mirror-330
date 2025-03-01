import requests
import json

class SMSMobileAPIEmailSender:
    """
    A Python module to send emails using SMSMobileAPI after linking your email account to the API.
    """

    def __init__(self, apikey: str, apikeybox: str):
        """
        Initializes the email sender with authentication details.
        :param apikey: Your unique API key for authentication.
        :param apikeybox: The API key linked to your email configuration.
        """
        self.api_url = "https://api.smsmobileapi.com/sendemail/"
        self.apikey = apikey
        self.apikeybox = apikeybox

    def send_email(self, sender_name: str, sender_email: str, recipient_email: str,
                   mail_subject: str, mail_body: str, allow_self_signed: str = "no",
                   unsubscribe: int = 0, email_cc: list = None,
                   attachment_base64: str = None, charset: str = "UTF-8",
                   embedded_image: str = None, embedded_image_cid: str = None,
                   format: str = None, reply_name: str = None, reply_email: str = None):
        """
        Sends an email through the SMSMobileAPI email service.
        :param sender_name: Name of the email sender.
        :param sender_email: Email address of the sender.
        :param recipient_email: Email address of the recipient.
        :param mail_subject: Subject of the email.
        :param mail_body: Content of the email (HTML or plain text).
        :param allow_self_signed: Set to "yes" to allow self-signed certificates.
        :param unsubscribe: Set to 1 to activate unsubscribe link.
        :param email_cc: List of additional email addresses to CC (max 3).
        :param attachment_base64: Base64-encoded attachment content.
        :param charset: Character set for the email. Default is UTF-8.
        :param embedded_image: URL of the image to be embedded.
        :param embedded_image_cid: Content-ID (CID) for referencing the embedded image.
        :param format: Response format.
        :param reply_name: The name of the reply sender.
        :param reply_email: The email address of the reply sender.
        :return: API response in JSON format.
        """
        payload = {
            "apikey": self.apikey,
            "apikeybox": self.apikeybox,
            "sender_name": sender_name,
            "sender_email": sender_email,
            "recipient_email": recipient_email,
            "mail_subject": mail_subject,
            "mail_body": mail_body,
            "allow_self_signed": allow_self_signed,
            "unsubscribe": unsubscribe,
            "charset": charset,
            "from_source":"python"
        }
        
        if email_cc:
            for i, cc in enumerate(email_cc[:3]):  # Only allow max 3 CC emails
                payload[f"email_cc{i + 1}"] = cc

        if attachment_base64:
            payload["attachmentBase64"] = attachment_base64
        if embedded_image:
            payload["embeddedImage"] = embedded_image
        if embedded_image_cid:
            payload["embeddedImage_cid"] = embedded_image_cid
        if format:
            payload["format"] = format
        if reply_name:
            payload["reply_name"] = reply_name
        if reply_email:
            payload["reply_email"] = reply_email

        headers = {"Content-Type": "application/json"}
        response = requests.post(self.api_url, data=json.dumps(payload), headers=headers)
        return response.json()

