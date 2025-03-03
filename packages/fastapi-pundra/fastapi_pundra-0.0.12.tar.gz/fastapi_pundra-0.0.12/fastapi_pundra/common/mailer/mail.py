from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
from .mail_templating import EmailTemplates
from fastapi_pundra.common.helpers import base_path
import os
from typing import List

# Load environment variables from .env file
load_dotenv()


# Configure email connection
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_FROM=os.getenv('MAIL_FROM_ADDRESS'),  # Ensure this is a valid email address
    MAIL_PORT=int(os.getenv('MAIL_PORT')),
    MAIL_SERVER=os.getenv('MAIL_HOST'),
    MAIL_STARTTLS=False,  # or False based on your configuration
    MAIL_SSL_TLS=False,   # or False based on your configuration
    USE_CREDENTIALS=True
)

def render_mail_template(template_name: str, context: dict = {}):
    # Initialize EmailTemplates with the correct directory
    project_base_path = os.getenv('PROJECT_BASE_PATH', 'app')

    template_dir = os.path.join(base_path(), project_base_path, 'templates', 'mails')
    templates = EmailTemplates(directory=template_dir)
    # Render the specified template with the given context
    return templates.render_template(template_name, context)

async def send_mail_util(subject: str, to: List[str], template_name: str, context: dict = None, cc: List[str] | str = None, bcc: List[str] | str = None, reply_to: List[str] | str = None):
    try:
        if not isinstance(to, list):
            to = [to]
            
        message = MessageSchema(
            subject=subject,
            recipients=to,
            body=render_mail_template(template_name=template_name, context=context),
            subtype="html"
        )
        
        fm = FastMail(conf)
        await fm.send_message(message)
        return "Email has been sent"
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return f'An error occurred while sending the email: {str(e)}'

async def send_mail_background(background_tasks: BackgroundTasks, subject: str, to: List[str], template_name: str, context: dict = None, cc: List[str] | str = None, bcc: List[str] | str = None, reply_to: List[str] | str = None):
    background_tasks.add_task(send_mail_util, subject, to, template_name, context, cc, bcc, reply_to)
    return "Email scheduled for sending"

async def send_mail(subject: str, to: List[str], template_name: str, context: dict = None, cc: List[str] | str = None, bcc: List[str] | str = None, reply_to: List[str] | str = None):
    return await send_mail_util(subject, to, template_name, context, cc, bcc, reply_to)

