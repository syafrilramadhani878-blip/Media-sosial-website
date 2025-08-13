import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.gmail_email = os.environ.get('GMAIL_EMAIL', 'Mochsyafrilramadhani5@gmail.com')
        self.gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_contact_message(self, name: str, sender_email: str, message: str) -> bool:
        """
        Send contact form message to the owner's email
        """
        try:
            if not self.gmail_password:
                logger.error("Gmail App Password not configured")
                return False

            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.gmail_email
            msg['To'] = self.gmail_email
            msg['Subject'] = f"Pesan Baru dari Website - {name}"

            # Email body
            email_body = f"""
Anda menerima pesan baru dari website Anda:

📧 Dari: {name}
📩 Email: {sender_email}
📅 Waktu: {datetime.now().strftime('%d %B %Y, %H:%M WIB')}

💬 Pesan:
{message}

---
Pesan ini dikirim secara otomatis dari website profil sosial media Anda.
            """

            msg.attach(MIMEText(email_body, 'plain'))

            # Connect to Gmail SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Enable security
            server.login(self.gmail_email, self.gmail_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.gmail_email, self.gmail_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully from {sender_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("Gmail authentication failed. Check email and app password.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def test_connection(self) -> bool:
        """
        Test email connection without sending
        """
        try:
            if not self.gmail_password:
                return False
                
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.gmail_email, self.gmail_password)
            server.quit()
            return True
        except Exception as e:
            logger.error(f"Email connection test failed: {str(e)}")
            return False

# Global instance
email_service = EmailService()