# notifications.py

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

# Configure logging
logging.basicConfig(filename=config.LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class NotificationManager:
    @staticmethod
    def log_info(message):
        """Log an informational message."""
        logging.info(message)

    @staticmethod
    def log_error(message):
        """Log an error message."""
        logging.error(message)

    @staticmethod
    def print_message(message, level="INFO"):
        """Print a message to the console and log it."""
        if level.upper() == "INFO":
            print(f"[INFO] {message}")
            NotificationManager.log_info(message)
        elif level.upper() == "ERROR":
            print(f"[ERROR] {message}")
            NotificationManager.log_error(message)

    @staticmethod
    def send_email(subject, body):
        """Send an email notification."""
        if not config.EMAIL_NOTIFICATIONS_ENABLED:
            NotificationManager.print_message("Email notifications are disabled in the configuration.", "INFO")
            return

        try:
            msg = MIMEMultipart()
            msg["From"] = config.EMAIL_SENDER
            msg["To"] = config.EMAIL_RECEIVER
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            # Set up the SMTP server
            with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
                server.starttls()
                server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
                server.send_message(msg)

            NotificationManager.print_message(f"Email sent successfully: {subject}", "INFO")
        except Exception as e:
            NotificationManager.print_message(f"Error sending email: {e}", "ERROR")


# Example usage
if __name__ == "__main__":
    NotificationManager.print_message("This is an info log.")
    NotificationManager.print_message("This is an error log.", "ERROR")

    # Example email
    NotificationManager.send_email(
        subject="Workflow Update: Preprocessing Completed",
        body="The data preprocessing step has been successfully completed."
    )
