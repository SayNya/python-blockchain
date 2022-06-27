from src.ellipse.base import Point
from src.ellipse.hash import hash160, encode_base58_checksum
from src.ellipse.secp256k1.constants import A, B, N, P
from src.ellipse.secp256k1.secp256k1_field import S256Field
from src.ellipse.signature import Signature

S256Coordinate = S256Field | int | None


class S256Point(Point):

    def __init__(self, x: S256Coordinate, y: S256Coordinate, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        if not self.x:
            return "S256Point(infinity)"
        return f"S256Point({self.x}, {self.y})"

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def verify(self, z: int, sig: Signature):
        s_inv = pow(sig.s, N - 2, N)
        
        u = z * s_inv % N
        v = sig.r * s_inv % N

        total = u * G + v * self
        return total.x.num == sig.r

    def sec(self, compressed=True):
        x_bytes = self.x.num.to_bytes(32, "big")
        if compressed:
            prefix = b"\x03" if self.y.num % 2 else b"\x02"
            return prefix + x_bytes
        return b"\x04" + x_bytes + self.y.num.to_bytes(32, "big")

    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        h160 = self.hash160(compressed)
        prefix = b"\x6f" if testnet else b"\x00"
        return encode_base58_checksum(prefix + h160)

    @classmethod
    def parse(cls, sec_bin):
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], "big")
            y = int.from_bytes(sec_bin[33:65], "big")
            return S256Point(x=x, y=y)
        is_even = sec_bin[0] == 2
        x = S256Field(int.from_bytes(sec_bin[1:], "big"))
        alpha = x ** 3 + S256Field(B)
        beta = alpha.sqrt()
        if beta.num % 2:
            even_beta = S256Field(P - beta.num)
            odd_beta = beta
        else:
            even_beta = beta
            odd_beta = S256Field(P - beta.num)
        if is_even:
            return S256Point(x, even_beta)
        return S256Point(x, odd_beta)


G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
)
