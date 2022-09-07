import logging
from django.core.mail.message import EmailMessage
from penpal.celery import app


logger = logging.getLogger(__name__)


@app.task()
def send_email(subject, body, to):
    mail = EmailMessage(subject=subject, body=body, to=[to])
    try:
        mail.send()
        logger.info(f"Mail has been sent to {to}")
    except Exception as e:
        logger.error(f"Mail couldn't be sent to {to}. Error: {e}")
