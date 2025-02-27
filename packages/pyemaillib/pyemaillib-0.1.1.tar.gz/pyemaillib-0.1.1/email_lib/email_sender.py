from typing import Literal, Optional, List, Tuple, Union
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from jinja2 import Environment
import logging
import os

logger = logging.getLogger(__name__)

def render_template(env: Environment, template_name: str, **context) -> str:
    """Renders an email template dynamically."""
    template = env.get_template(template_name)
    return template.render(**context)

MailTextType = Literal["plain", "html"]

class EmailSender:
    def __init__(self, smtp_host: str, smtp_user: str, smtp_pass: str, from_email: str):
        self.smtp_host = smtp_host
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.from_email = from_email

    async def send_email(
        self,
        text: str,
        to_email: str,
        subject: str,
        text_type: MailTextType = "plain",
        attachments: Optional[List[Union[str, Tuple[str, str]]]] = None,  # Now supports single file paths too
    ) -> bool:
        """Sends an email using SMTP with optional file attachments."""
        try:
            # Prepare email
            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = to_email
            msg["Date"] = formatdate(localtime=True)
            msg["Subject"] = subject
            msg.attach(MIMEText(text, text_type))

            # Attach files if provided
            if attachments:
                for attachment in attachments:
                    if isinstance(attachment, str):
                        filepath = attachment
                        filename = os.path.basename(filepath)  # Default to actual file name
                    else:
                        filepath, filename = attachment

                    if not os.path.exists(filepath):
                        logger.warning(f"Attachment not found: {filepath}")
                        continue

                    with open(filepath, "rb") as f:
                        part = MIMEApplication(f.read(), Name=filename)
                    part["Content-Disposition"] = f'attachment; filename="{filename}"'
                    msg.attach(part)

            # Send email
            smtp = smtplib.SMTP(self.smtp_host)
            smtp.starttls()
            smtp.login(user=self.smtp_user, password=self.smtp_pass)
            smtp.sendmail(self.from_email, to_email, msg.as_string())
            smtp.quit()

            logger.info("Email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
