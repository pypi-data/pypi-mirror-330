from __future__ import annotations

import typing as t

from joserfc.jwe import decrypt_compact
from joserfc.jwe import encrypt_compact
from joserfc.jwk import OctKey
from joserfc.util import to_str

AlgorithmTypes = t.Literal["A128KW", "A256KW"]
EncryptionTypes = t.Literal["A128GCM", "A192KW", "A256GCM"]
DEFAULT_ALGORITHM: AlgorithmTypes = "A128KW"
DEFAULT_ENCRYPTION: EncryptionTypes = "A128GCM"


def encrypt(
    content: bytes | str,
    key: OctKey,
    algorithm: AlgorithmTypes = DEFAULT_ALGORITHM,
    encryption: EncryptionTypes = DEFAULT_ENCRYPTION,
) -> str:
    protected = {"alg": algorithm, "enc": encryption}
    return encrypt_compact(protected, content, key)


def decrypt(content: bytes | str, key: OctKey) -> bytes:
    obj = decrypt_compact(content, key)
    assert isinstance(obj.plaintext, bytes)
    return obj.plaintext


def parse_content(content: bytes) -> dict[str, str]:
    """Parsing the given content into key value pairs. The ``content``
    should be bytes or str in the bellow syntax::

        key_1: value - 1
        key_2: value - 2

        # use # for commenting
        key_3: value - 3

    :param content: content in bytes
    :return: dict[str, str]
    """
    text = to_str(content)

    rv: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        try:
            k, v = line.split(":", 1)
            rv[k.strip()] = v.strip()
        except ValueError:
            continue
    return rv


def import_key(key: str, algorithm: AlgorithmTypes) -> OctKey:
    if algorithm == "A128KW":
        key_bit_size = 128
    else:
        key_bit_size = 256

    key_size = key_bit_size // 8

    if len(key) < key_size:
        key = key + " " * (key_size - len(key))
    elif len(key) > key_size:
        key = key[:key_size]
    return OctKey.import_key(key)
