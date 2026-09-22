#!/usr/bin/env python3
"""CIDv1 self-check: 'b' + base32-lower(no pad) of header 01551220 || sha256."""
import base64
import hashlib
import sys

def cidv1(data: bytes) -> str:
    digest = hashlib.sha256(data).digest()
    prefix = bytes.fromhex("01551220")
    return "b" + base64.b32encode(prefix + digest).decode("ascii").lower().rstrip("=")

data = open(sys.argv[1], "rb").read()
got = cidv1(data)
print(got)
if len(sys.argv) > 2:
    ok = (got == sys.argv[2])
    print("MATCH" if ok else "MISMATCH")
    sys.exit(0 if ok else 1)
