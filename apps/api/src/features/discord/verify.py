from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


def verify_signature(
    public_key: str, signature: str, timestamp: str, body: bytes
) -> bool:
    if not public_key:
        return False
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key))
        verify_key.verify(timestamp.encode() + body, bytes.fromhex(signature))
    except (BadSignatureError, ValueError):
        return False
    return True
