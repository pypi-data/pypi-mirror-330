import base64
import os

from urllib.parse import urlparse

from freezegun import freeze_time
import pytest

from pfpy.auth.utils import (
    check_for_url_tampering,
    construct_signature_header_bytes_to_sign,
    construct_signature_url_bytes_to_sign,
    get_sig_header_components,
    get_signature_from_url,
    parse_signature_header,
    resolve_security_key,
    validate_signature,
)

from tests.helpers import create_signed_request_headers_with_body, create_signed_request_url
from tests.mock_test_data import INVALID_AUTH_HEADER, VALID_AUTH_HEADER


def test_resolve_security_key(custom_environment: pytest.MonkeyPatch):
    """Tests that the security key can be retrieved from the environment."""

    key_from_environment = os.getenv("PASSFORT_INTEGRATION_SECRET_KEY")
    assert key_from_environment == "pVuQv2AK2xR3Az4ZeAfEgoUTXbTWRH4bRnxEsLkQwsI="
    assert base64.b64decode(key_from_environment) == resolve_security_key()


def test_get_sig_header_components(custom_environment: pytest.MonkeyPatch):
    """Tests that the signature header components can be extracted from the header string."""

    key_id, algorithm, signature, signed_headers = get_sig_header_components(VALID_AUTH_HEADER)
    assert key_id == "pVuQv2AK"
    assert algorithm == "hs2019"
    assert signature == "fLrCxvGbmniwADXVgIRfA3n1x5oB4XZhSdx7u8ZdhVw="
    assert signed_headers == "(request-target) host date digest"

    with pytest.raises(ValueError) as excinfo:
        get_sig_header_components(INVALID_AUTH_HEADER)
    assert "Malformed authorization header" in str(excinfo.value)


def test_parse_signature_header_valid(custom_environment: pytest.MonkeyPatch):
    """Tests that the signature header can be parsed correctly."""

    request_url = f"http://{os.getenv('DOMAIN')}/passfort-integration/checks"
    parsed_header = parse_signature_header(urlparse(request_url), VALID_AUTH_HEADER)
    assert parsed_header.key_id == "pVuQv2AK"
    assert parsed_header.algorithm == "hs2019"
    assert parsed_header.signature == "fLrCxvGbmniwADXVgIRfA3n1x5oB4XZhSdx7u8ZdhVw="
    assert parsed_header.signed_headers == ["(request-target)", "host", "date", "digest"]


def test_parse_signature_header_invalid(custom_environment: pytest.MonkeyPatch):
    """Tests that a signature signed with an unsupported algorithm is deemed invalid."""

    request_url = f"http://{os.getenv('DOMAIN')}/passfort-integration/checks"

    with pytest.raises(ValueError) as excinfo:
        parse_signature_header(urlparse(request_url), None)
    assert "Missing authorization header." in str(excinfo.value)

    sig_header_with_wrong_algo = 'Signature keyId="pVuQv2AK",algorithm="FAIL",signature="fLrCxvGbmniwADXVgIRfA3n1x5oB4XZhSdx7u8ZdhVw=",headers="(request-target) host date digest"'

    with pytest.raises(ValueError) as excinfo:
        parse_signature_header(urlparse(request_url), sig_header_with_wrong_algo)
    assert "Unsupported signature algorithm" in str(excinfo.value)


@freeze_time("Tue, 28 May 2024 11:49:13 UTC", tz_offset=0)
def test_validate_signature_valid(custom_environment: pytest.MonkeyPatch):
    """Tests that a valid signature is correctly determined as valid."""

    request_url = f"http://{os.getenv('DOMAIN')}/passfort-integration/checks"
    parsed_url = urlparse(request_url)

    request_headers = create_signed_request_headers_with_body()

    parsed_sig_header = parse_signature_header(
        parsed_url,
        request_headers.get("authorization"),
    )

    bytes_to_sign = construct_signature_header_bytes_to_sign(
        parsed_url=parsed_url,
        method="post",
        sig_header=parsed_sig_header,
        raw_headers=request_headers,
    )

    assert validate_signature(parsed_sig_header.signature, bytes_to_sign, url_safe_decode=False)


def test_url_signature_invalid(custom_environment: pytest.MonkeyPatch):
    """Tests that tampered URLs are detected as invalid."""

    url = f"{os.getenv('DOMAIN')}/passfort-integration/external-resources/GB04366849/?version=1&valid_until=1716976440&auditee_id=ada1d906-0329-486f-aa5f-8f2376ed9376&signature=764Oknd2eH_MxRkehs8NKxMBokVENWPuz8JHM-qBcck%3D&valid_until=1716976441"

    with pytest.raises(ValueError) as excinfo:
        check_for_url_tampering(url)
    assert "URL has potentially been tampered with." in str(excinfo.value)


@freeze_time("Tue, 28 May 2024 11:49:13 UTC", tz_offset=0)
def test_signature_valid(custom_environment: pytest.MonkeyPatch):
    """Tests that a valid signed url is correctly determined as valid."""

    value = create_signed_request_url()
    bytes_to_sign = construct_signature_url_bytes_to_sign(value)
    received_signature: str = get_signature_from_url(value)
    assert validate_signature(received_signature, bytes_to_sign, url_safe_decode=True)
