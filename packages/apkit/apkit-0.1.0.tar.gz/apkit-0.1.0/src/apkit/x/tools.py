from typing import Optional

from apmodel import Actor, Multikey
from apmodel.security.cryptographickey import CryptographicKey

async def get_keys(actor: Actor, signature_header: Optional[str] = None):
    keys = {}
    if signature_header and isinstance(actor.publicKey, CryptographicKey):
        for item in signature_header.split(","):
            key, value = item.split("=", 1)
            if key == "keyId" and actor.publicKey.id == key:
                keys[value.strip().strip('"')] = actor.publicKey.publicKeyPem
    if actor.assertionMethod:
        for method in actor.assertionMethod:
            if isinstance(method, Multikey):
                keys[method.id] = method.publicKeyMultibase
    return keys