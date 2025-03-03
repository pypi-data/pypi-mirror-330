from celery import shared_task
from typing import List
import asyncio
from .mail import send_mail

@shared_task(name="pundra_send_email_queue_task")
def send_email_queue_task(subject: str, to: List[str], template_name: str, context: dict, cc: List[str] | str = None, bcc: List[str] | str = None, reply_to: List[str] | str = None):
    # Create and run the event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(send_mail(
            subject=subject,
            to=to,
            template_name=template_name,
            context=context,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to
        ))
        print(str(result))
        print(f"Sending email to {to} with subject {subject} and template {template_name} and context {context}")
        return "Email sent"
    finally:
        loop.close()