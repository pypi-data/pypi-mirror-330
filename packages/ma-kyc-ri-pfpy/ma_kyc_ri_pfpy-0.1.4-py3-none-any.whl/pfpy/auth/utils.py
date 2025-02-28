import base64
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os
import hashlib
import hmac
import re
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import ParseResult, parse_qs, quote, urlparse

from pfpy.types.parsed_signature_header import ParsedSignatureHeader


def resolve_security_key() -> bytes:
    """Resolves the security key from the environment."""

    key = os.getenv("PASSFORT_INTEGRATION_SECRET_KEY")
    if not key:
        raise ValueError("Missing security key.")
    return base64.b64decode(key)


def get_sig_header_components(auth_header: str) -> Tuple[str, str, str, str]:
    """Extracts the keyId, algorithm, signature, and signed headers from the authorization header."""

    pattern = r'Signature keyId="(.+?)",algorithm="(.+?)",signature="(.+?)",headers="(.+?)"'
    match = re.match(pattern, auth_header)

    if not match:
        raise ValueError(f"Malformed authorization header: '{auth_header}'")

    key_id, algorithm, signature, signed_headers = match.groups()

    return key_id, algorithm, signature, signed_headers


def parse_signature_header(parsed_url: ParseResult, auth_header: Optional[str]) -> ParsedSignatureHeader:
    """Parses the signature header and returns a validated ParsedSignatureHeader object."""

    if not auth_header and "signature" not in parsed_url.query:
        raise ValueError("Missing authorization header.")

    assert auth_header is not None

    key_id, algorithm, signature, signed_headers = get_sig_header_components(auth_header)

    if algorithm not in {"hmac-sha256", "hs2019"}:
        raise ValueError(f"Unsupported signature algorithm: {algorithm}")

    parsed_header = ParsedSignatureHeader(
        key_id=key_id,
        algorithm=algorithm,
        signature=signature,
        signed_headers=signed_headers.split(" "),
    )

    return parsed_header


def construct_signature_header_bytes_to_sign(
    parsed_url: ParseResult, sig_header: ParsedSignatureHeader, method: str, raw_headers: Dict[str, Any]
) -> bytes:
    """Constructs the bytes to sign for the signature header."""

    signing_parts: List[str] = []
    request_path = parsed_url.path

    for header in sig_header.signed_headers:
        value = (
            f"{method.lower()} {request_path}" if header.lower() == "(request-target)" else raw_headers.get(header, "")
        )
        signing_parts.append(f"{header.lower()}: {value}")

    bytes_to_sign: bytes = "\n".join(signing_parts).encode()

    return bytes_to_sign


def validate_signature(signature_to_check: str, bytes_to_sign: bytes, url_safe_decode: bool = False) -> bool:
    """Validates the signature against the bytes to sign."""

    secret_key = resolve_security_key()

    expected_signature = hmac.new(secret_key, bytes_to_sign, hashlib.sha256).digest()

    decoded_signature_to_check = (
        base64.urlsafe_b64decode(signature_to_check) if url_safe_decode else base64.b64decode(signature_to_check)
    )

    match = hmac.compare_digest(decoded_signature_to_check, expected_signature)

    if not match:
        raise ValueError(f"{'URL' if url_safe_decode else 'Header'} signature is invalid.")

    return True


def check_date_header_is_valid(date_header: str) -> bool:
    """Checks if the date header is valid."""

    parsed_date = parsedate_to_datetime(date_header)
    parsed_date_timestamp = parsed_date.replace(tzinfo=timezone.utc).timestamp()

    if parsed_date:
        if abs(time.time() - parsed_date_timestamp) > 30:
            raise ValueError("Date header too far from current time.")

    return True


def check_url_sig_has_not_expired(valid_until: int) -> bool:
    """Checks if the URL signature has not expired."""

    time_plus_mins = datetime.now(timezone.utc)
    current_time = int(time_plus_mins.timestamp())

    if not valid_until > current_time:
        raise ValueError("URL valid until time expired.")

    return True


def construct_signature_url_bytes_to_sign(request_url: str) -> bytes:
    """Constructs the bytes to sign for the URL signature."""
    bytes_to_sign = re.sub(r"&signature=.*", "", request_url).encode()
    return bytes_to_sign


def get_signature_from_url(request_url: str) -> str:
    """Extracts the signature from the URL."""

    parsed_url = urlparse(request_url)
    query_dict = parse_qs(parsed_url.query)
    received_signature: str = query_dict["signature"][0]
    return received_signature


def check_for_url_tampering(request_url: str):
    """Checks if the URL has been tampered with."""

    parsed_url = urlparse(request_url)
    query_params = parse_qs(parsed_url.query)

    url_without_signature = re.sub(r"&signature=.*", "", request_url)

    signature = query_params.pop("signature", None)

    assert signature is not None

    expected = f"{url_without_signature}&signature={quote(signature[0])}"

    if request_url != expected:
        raise ValueError("URL has potentially been tampered with.")
