from typing import Optional
from pydantic import BaseModel, field_validator

from pfpy.auth.utils import (
    check_for_url_tampering,
    check_url_sig_has_not_expired,
    construct_signature_url_bytes_to_sign,
    get_signature_from_url,
    validate_signature,
)


class ParsedSignedUrl(BaseModel):
    request_url: str
    version: str
    valid_until: str
    auditee_id: str
    signature: str
    custom_data: Optional[str] = None

    @field_validator("valid_until", mode="after")
    def ensure_valid_date_for_url_sig(cls, value: str) -> str:
        """Ensures that the URL has not expired based on the valid until param."""
        valid_until = int(value)
        check_url_sig_has_not_expired(valid_until)
        return value

    @field_validator("request_url", mode="after")
    def validate_url_sig(cls, value: str) -> str:
        """Checks to see if the URL signature is valid."""
        bytes_to_sign = construct_signature_url_bytes_to_sign(value)
        received_signature: str = get_signature_from_url(value)
        validate_signature(received_signature, bytes_to_sign, url_safe_decode=True)
        return value

    @field_validator("request_url", mode="after")
    def validate_url_untampered(cls, value: str) -> str:
        """Checks to see if the URL signature is valid."""
        check_for_url_tampering(value)
        return value
