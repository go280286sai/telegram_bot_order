from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from starlette.responses import HTMLResponse
from helps.help import is_valid_email
from helps.email_utils import send_html_email
import os

templates = Jinja2Templates(directory="templates")
env = Environment(loader=FileSystemLoader("templates"))
URL_SERVER = os.getenv("URL_SERVER")


async def create_subscriber_email(
        idx: int,
        email: str,
        hash_active: str
) -> bool:
    if not is_valid_email(email):
        return False

    confirmation_link = \
        f"{URL_SERVER}/subscriber/confirm/{int(idx)}/{hash_active}"
    template = env.get_template("confirm_email.html")
    html_content = template.render(confirmation_link=confirmation_link)

    return send_html_email(
        subject="Subscription confirmation",
        recipient=email,
        html_content=html_content
    )


async def send_emails(
        header: str,
        title: str,
        body: str,
        idx: int,
        email: str,
        hash_active: str,
        footer: bool = True
) -> bool:
    if not is_valid_email(email):
        return False
    destroy_link = f"{URL_SERVER}/subscriber/destroy/{int(idx)}/{hash_active}"
    template = env.get_template("send_message.html")
    html_content = template.render(
        destroy_link=destroy_link,
        header=header,
        title=title,
        body=body,
        host=os.getenv("SMTP_SERVER"),
        footer=footer
    )

    return send_html_email(
        subject=title,
        recipient=email,
        html_content=html_content
    )


async def register_user_confirm(
        idx: int,
        email: str,
        hash_active: str
) -> bool:
    register_link = f"{URL_SERVER}/user/confirm/{int(idx)}/{hash_active}"
    template = env.get_template("register_email.html")
    html_content = template.render(
        register_link=register_link,
        host=os.getenv("SMTP_SERVER")
    )

    return send_html_email(
        subject="Registration confirmation",
        recipient=email,
        html_content=html_content
    )


async def confirm_email() -> HTMLResponse:
    template = env.get_template("confirm_email_success.html")
    html_content = template.render()
    return HTMLResponse(content=html_content)
