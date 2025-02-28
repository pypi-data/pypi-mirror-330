import typing_extensions
from pydantic import BaseModel, field_validator, model_validator
from urllib.parse import urlparse
from typing import Dict, Optional

from pfpy.auth.utils import (
    check_date_header_is_valid,
    construct_signature_header_bytes_to_sign,
    parse_signature_header,
    validate_signature,
)


class ParsedSignedHeaderRequest(BaseModel):
    method: str
    request_url: str
    request_method: Optional[str]
    headers: Dict[str, str]

    @field_validator("headers", mode="after")
    def validate_date_header(cls, value: Dict[str, str]) -> Dict[str, str]:
        """Ensures the date header is within 30 seconds of the current time."""
        auth_header = value.get("authorization")
        date_header = value.get("date")

        if auth_header and date_header:
            check_date_header_is_valid(date_header)

        return value

    @model_validator(mode="after")
    def validate_auth_header_sig(self) -> typing_extensions.Self:

        parsed_url = urlparse(self.request_url)
        auth_header = self.headers.get("authorization")

        parsed_signature_header = parse_signature_header(parsed_url, auth_header)

        bytes_to_sign = construct_signature_header_bytes_to_sign(
            parsed_url=parsed_url,
            method=self.method,
            sig_header=parsed_signature_header,
            raw_headers=self.headers,
        )

        validate_signature(parsed_signature_header.signature, bytes_to_sign, url_safe_decode=False)

        return self
