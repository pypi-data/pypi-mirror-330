from typing import List
from pydantic import BaseModel


class ParsedSignatureHeader(BaseModel):
    key_id: str
    algorithm: str
    signature: str
    signed_headers: List[str]