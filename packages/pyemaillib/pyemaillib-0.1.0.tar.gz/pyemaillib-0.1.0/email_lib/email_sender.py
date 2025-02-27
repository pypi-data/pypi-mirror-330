
import smtplib
#from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from random import randint
from datetime import timedelta
from jinja2 import Environment
import logging

logger = logging.getLogger(__name__)

def render_template(env: Environment, template_name: str, **context) -> str:
    """Renders an email template dynamically."""
    template = env.get_template(template_name)
    return template.render(**context)


async def send_email(text: str, from_email: str, to_email: str, subject: str,
                     smtp_host: str, smtp_user: str, smtp_pass: str) -> bool:
    """Sends an email using SMTP with a provided text bodypypi-AgEIcHlwaS5vcmcCJGFkNGQ0ODdmLTkzNmEtNDFlMy05YTA4LTdiMTA0ZTAwMmUyZgACKlszLCJhYWM0OGMzYS1iNGE2LTQ3MTgtODRjYS02YmRiZTQxYTg2YzIiXQAABiAh7c-PLBnLkvoBYxnPXWY6TcWM6ChKEIclwOHpPoJQKw."""
    try:
        # Prepare email
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(text, 'plain'))
        
        # Send email
        smtp = smtplib.SMTP(smtp_host)
        smtp.starttls()
        smtp.login(user=smtp_user, password=smtp_pass)
        smtp.sendmail(from_email, to_email, msg.as_string())
        smtp.quit()
        
        logger.info('Email sent successfully')
        return True
    except Exception as e:
        logger.error(f'Failed to send email: {str(e)}')
        return False
    
    