import hashlib
import hmac

from src.ellipse.hash import encode_base58_checksum, hash256_hex
from src.ellipse.secp256k1.constants import N
from src.ellipse.secp256k1.secp256k1_point import G
from src.ellipse.signature import Signature


class PrivateKey:

    def __init__(self, secret: int):
        self.secret = secret
        self.point = secret * G

    def hex(self):
        return "{:x}".format(self.secret).zfill(64)

    def sign(self, z: int):
        k = self.deterministic_k(z)
        r = (k * G).x.num
        k_inv = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_inv % N
        if s > N / 2:
            s = N - s
        return Signature(r, s)

    def deterministic_k(self, z: int):
        k = b"\x00" * 32
        v = b"\x01" * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, "big")
        secret_bytes = self.secret.to_bytes(32, "big")
        s256 = hashlib.sha256
        k = hmac.new(k, v + b"\x00" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b"\x01" + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, "big")
            if 1 <= candidate < N:
                return candidate
            k = hmac.new(k, v + b"\x00", s256).digest()
            v = hmac.new(k, v, s256).digest()

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, "big")

        prefix = b"\xef" if testnet else b"\x80"
        suffix = b"\x01" if compressed else b""

        return encode_base58_checksum(prefix + secret_bytes + suffix)


my_key = PrivateKey(0xfffffffffffffffffffff10ffffffffebaaedce6af48a03bbfd25e8cd0364141)

text = "Hello, World".encode("utf-8")
print(text)
text_hash = hash256_hex(text)
print(text_hash)
signature = my_key.sign(text_hash)
print(signature.r, signature.s)
print(my_key.point.verify(text_hash, signature))
