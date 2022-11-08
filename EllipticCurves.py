import random
from typing import Union, Tuple
import math_helpers

ProjectivePoint = Tuple[int, int, int]

POINT_AT_INFIITY = (0,1,0)

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
        n = self.modulus
        return (x % n, y % n, 1)

    def multiply_point(self, multiplicand: int, point: ProjectivePoint):
        prod = POINT_AT_INFIITY
        for i in range(multiplicand):
            prod = self.add_points(prod, point)
        return prod

    def add_points(self, p1: ProjectivePoint, p2: ProjectivePoint) -> Union[ProjectivePoint, int]:
        """
        Adds two points on the curve. 
        If the point addition fails, returns the number which had no inverse mod n
        """
        if is_infinity(p1):
            return p2
        if is_infinity(p2):
            return p1

        n = self.modulus
        x1, y1, _ = p1
        x2, y2, _ = p2
        if p1 == p2:
            if y1 == 0:
                x3, y3, z3 = POINT_AT_INFIITY    
            else:
                denom = 2 * y1
                inv = math_helpers.mult_inverse(denom, n)
                if inv is None:
                    return denom
                m = (3 * x1**2 + self.A) * inv
                x3 = m**2 - 2* x1
                y3 = m * (x1-x3) - y1
                z3 = 1
        else:
            if x1 != x2:
                denom = x2 - x1
                inv = math_helpers.mult_inverse(denom, n)
                if inv is None:
                    return denom
                m = (y2 - y1) * inv
                x3 = m**2 - x1 - x2
                y3 = m * (x1 - x3) - y1
                z3 = 1
            else:
                x3, y3, z3 = POINT_AT_INFIITY
        return x3 % n, y3 % n, z3 % n


    def rand_curve_and_point_mod_n(n: int):
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
