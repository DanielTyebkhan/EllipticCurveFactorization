import random
from typing import Tuple

ProjectivePoint = Tuple[int, int, int]

POINT_AT_INFIITY = (0,0,0)

def is_infinity(point: ProjectivePoint) -> bool:
    return point == POINT_AT_INFIITY


class EllipticCurveModN:
    """
    Weierstrass representation of elliptic curve group addition over integer rings mod n
    Formulas from Washington
    """
    def __init__(self, a: int, b: int, modulus: int):
        self.A = a
        self.B = b
        self.modulus = modulus
    
    def point(self, x: int, y: int) -> ProjectivePoint:
        return (x % self.modulus, y % self.modulus, 1)

    def add_points(self, p1: ProjectivePoint, p2: ProjectivePoint) -> ProjectivePoint:
        if is_infinity(p1):
            return p2
        if is_infinity(p2):
            return p1

        x1, y1, z1 = p1
        x2, y2, z2 = p2
        if p1 == p2:
            if y1 == 0:
                x3, y3, z3 = POINT_AT_INFIITY    
            else:
                m = (3 * x1**2 + self.A) / (2 * y1)
                x3 = m**2 - 2* x1
                y3 = m * (x1-x3) - y1
                z3 = 1
        else:
            if x1 != x2:
                m = (y2 - y1) / (x2 - x1)
                x3 = m**2 - x1 - x2
                y3 = m * (x1 - x3) - y1
                z3 = 1
            else:
                x3, y3, z3 = POINT_AT_INFIITY
        return x3, y3, z3


    def rand_curve_and_point_mod_n(n):
        '''
        Algorithm from Washington, page 192
        '''
        A = random.randint(0, n)
        u = random.randint(0, n)
        v = random.randint(0, n)
        C = (v**2 - u**3 - A*u) % n
        curve = EllipticCurveModN(A, C, n)
        point = curve.point(u, v)
        return curve, point

    def __str__(self) -> str:
        return f'y^2 = x^3 + {self.A}x + {self.B} over Z mod {self.modulus}'

    def __repr__(self) -> str:
        return self.__str__()
