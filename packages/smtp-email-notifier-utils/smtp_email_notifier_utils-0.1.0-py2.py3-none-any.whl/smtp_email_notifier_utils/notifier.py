import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email configuration from environment variables
SMTP_ADDRESS = os.getenv("SMTP_ADDRESS")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
EMAIL_ID = os.getenv("EMAIL_ID")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_notification(to_address: str, subject: str, message: str) -> bool:
    """
    Send a notification email to the specified address.

    Args:
        to_address (str): Recipient's email address
        subject (str): Email subject line
        message (str): Email body text

    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Create MIMEText object with the message
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = EMAIL_ID
        msg["To"] = to_address

        # Establish connection with SMTP server
        with smtplib.SMTP(SMTP_ADDRESS, SMTP_PORT) as server:
            # Start TLS encryption
            server.starttls()

            # Login to the SMTP server
            server.login(EMAIL_ID, EMAIL_PASSWORD)

            # Send the email
            server.send_message(msg)

        return True

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


# Optional: Test the function if run directly
if __name__ == "__main__":
    # Example usage
    test_to = "test@example.com"
    test_subject = "Test Notification"
    test_message = "This is a test notification email."
    success = send_notification(test_to, test_subject, test_message)
    print(f"Email sent successfully: {success}")
