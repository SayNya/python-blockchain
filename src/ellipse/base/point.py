from src.ellipse.base import FieldElement

PointCoordinate = FieldElement | None


class Point:

    def __init__(self, x: PointCoordinate, y: PointCoordinate, a: FieldElement, b: FieldElement):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if not self.x and not self.y:
            return
        if self.y ** 2 != self.x ** 3 + a * x + b:
            raise ValueError(f"({x}, {y}) is not on the curve")

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        if not self.x:
            return "Point(infinity)"
        if isinstance(self.x, FieldElement):
            return f"Point({self.x.num},{self.y.num})_{self.a.num}_{self.b.num} FieldElement({self.x.prime})"
        return f"Point({self.x},{self.y})_{self.a}_{self.b}"

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError("Points {}, {} are not on the same curve".format(self, other))

        if not self.x:
            return other
        if not other.x:
            return self

        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)

        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x = s ** 2 - self.x - other.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)

        if self == other:
            s = (3 * self.x ** 2 + self.a) / (2 * self.y)
            x = s ** 2 - 2 * self.x
            y = s * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)

    def __rmul__(self, coefficient):
        coef = coefficient
        current = self
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result
