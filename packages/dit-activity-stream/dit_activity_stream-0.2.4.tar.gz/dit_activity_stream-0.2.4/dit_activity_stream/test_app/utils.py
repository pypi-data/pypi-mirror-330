from typing import Any, Dict, Literal

from django.conf import settings
from mohawk import Sender

HAWK_ID = settings.DJANGO_HAWK["HAWK_INCOMING_ACCESS_KEY"]
HAWK_SECRET = settings.DJANGO_HAWK["HAWK_INCOMING_SECRET_KEY"]


def hawk_auth_header(
    key_id: str,
    secret_key: str,
    url: str,
    method: Literal["GET"],
    content: bytes,
    content_type: str,
) -> Sender:
    return Sender(
        {
            "id": key_id,
            "key": secret_key,
            "algorithm": "sha256",
        },
        url,
        method,
        content=content,
        content_type=content_type,
    ).request_header


def get_hawk_kwargs(
    path: str, hawk_secret: str = HAWK_SECRET, forwarded: bool = False
) -> Dict[str, Any]:
    host = "localhost:8000"
    url = f"http://{host}{path}"

    hawk_kwargs: Dict[str, Any] = {
        "content_type": None,
        "HTTP_HOST": host,
        "HTTP_AUTHORIZATION": hawk_auth_header(
            key_id=HAWK_ID,
            secret_key=hawk_secret,
            url=url,
            method="GET",
            content=b"",
            content_type="",
        ),
    }

    if forwarded:
        hawk_kwargs.update(HTTP_X_FORWARDED_FOR="")

    return hawk_kwargs
