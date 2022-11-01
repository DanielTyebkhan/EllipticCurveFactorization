import random
from typing import Tuple

ProjectivePoint = Tuple[int, int, int]

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
        return (x, y, 0)

    def add_points(self, p1: ProjectivePoint, p2: ProjectivePoint) -> ProjectivePoint:
        x1, y1, z1 = p1
        x2, y2, z2 = p2
        x1y2mx2y1 = x1 * y1 - x2*y1

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
