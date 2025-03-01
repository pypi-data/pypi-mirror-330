import unittest
from smsmobileapi_send_email.email_sender import SMSMobileAPIEmailSender

class TestSMSMobileAPIEmailSender(unittest.TestCase):

    def setUp(self):
        self.sender = SMSMobileAPIEmailSender("dummy_api_key", "dummy_apikeybox")

    def test_send_email(self):
        response = self.sender.send_email(
            sender_name="Test Sender",
            sender_email="test@example.com",
            recipient_email="recipient@example.com",
            mail_subject="Unit Test Email",
            mail_body="This is a test email.",
        )
        self.assertIsInstance(response, dict)

if __name__ == "__main__":
    unittest.main()
