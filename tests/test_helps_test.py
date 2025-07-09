import smtplib

import helps.help
from helps.help import (is_valid_email, validate_password,
                        hash_password, generate_transaction)
from helps.emails import (register_user_confirm, confirm_email,
                          send_emails, create_subscriber_email)
from helps.email_utils import send_html_email
import pytest
from starlette.responses import HTMLResponse


def test_is_email_valid():
    assert is_valid_email("Hello") is False
    assert is_valid_email("Hello.com") is False
    assert is_valid_email("Hello@com") is False
    assert is_valid_email("") is False
    assert is_valid_email("admin@admin.com") is True


def test_password():
    password = "qwertyQWE123!"
    assert hash_password(password) != password
    assert len(hash_password(password)) == 64
    assert validate_password(password) is True
    assert validate_password("12345") is False
    assert validate_password("qwerty") is False
    assert validate_password("qwerty12345") is False


def test_generate_transaction():
    assert isinstance(generate_transaction(), str)
    assert len(generate_transaction()) == 20


class DummySMTP:
    def __init__(self, *args, **kwargs):
        pass

    def starttls(self): pass

    def login(self, user, password): pass

    def sendmail(self, from_addr, to_addrs, msg): pass

    def quit(self): pass

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb): pass


@pytest.mark.parametrize("use_ssl", [True, False])
def test_send_html_email(monkeypatch, use_ssl):
    monkeypatch.setattr(smtplib, "SMTP", DummySMTP)
    monkeypatch.setattr(smtplib, "SMTP_SSL", DummySMTP)

    global SMTP_USER, SMTP_PASSWORD, SMTP_SERVER, SMTP_PORT
    SMTP_USER = "test@example.com"
    SMTP_PASSWORD = "secure-password"
    SMTP_SERVER = "smtp.example.com"
    SMTP_PORT = 465 if use_ssl else 587

    result = send_html_email(
        subject="Test Email",
        recipient="recipient@example.com",
        html_content="<h1>Hello</h1>"
    )
    assert result is True


@pytest.mark.asyncio
async def test_create_subscriber(monkeypatch):
    def mock_is_valid_email(email):
        return True

    def mock_send_html_email(subject, recipient, html_content):
        return True

    monkeypatch.setattr(helps.emails, "is_valid_email", mock_is_valid_email)
    monkeypatch.setattr(helps.emails, "send_html_email", mock_send_html_email)

    result = await create_subscriber_email(1, "admin", "dfgf")
    assert result is True


@pytest.mark.asyncio
async def test_register_user_confirm(monkeypatch):
    def mock_send_html_email(subject, recipient, html_content):
        return True

    monkeypatch.setattr(helps.emails, "send_html_email", mock_send_html_email)
    result = await register_user_confirm(1, "admin", "dfgf")
    assert result is True


@pytest.mark.asyncio
async def test_send_email(monkeypatch):
    def mock_send_html_email(subject, recipient, html_content):
        return True

    def mock_is_valid_email(email):
        return True

    monkeypatch.setattr(helps.emails, "is_valid_email", mock_is_valid_email)
    monkeypatch.setattr(helps.emails, "send_html_email", mock_send_html_email)
    result = await send_emails("<EMAIL>", "admin", "dfgf", 1, "email", "")
    assert result is True


@pytest.mark.asyncio
async def test_confirm_email(monkeypatch):
    result = await confirm_email()
    assert isinstance(result, HTMLResponse)
