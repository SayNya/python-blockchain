from src.ellipse.base import FieldElement
from src.ellipse.secp256k1.constants import P


class S256Field(FieldElement):

    def __init__(self, num: int, prime=None):
        super().__init__(num=num, prime=P)

    def __repr__(self):
        return "{:x}".format(self.num).zfill(64)

    def sqrt(self):
        return self ** ((P + 1) // 4)
