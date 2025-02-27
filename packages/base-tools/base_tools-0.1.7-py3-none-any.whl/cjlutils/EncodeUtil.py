import hashlib
import base64
import urllib.parse


def encode_md5(message: bytes) -> None | bytes:
    if message is None:
        return None
    return hashlib.md5(message).digest()


def encode_base64(message: bytes) -> None | bytes:
    if message is None:
        return None
    return base64.b64encode(message)


def decode_base64(message: bytes) -> None | bytes:
    if message is None:
        return None
    return base64.b64decode(message)


def encode_url(url: str) -> None | str:
    if url is None:
        return None
    return urllib.parse.quote_plus(url)


def decode_url(url: str) -> None | str:
    if url is None:
        return None
    return urllib.parse.unquote_plus(url)
