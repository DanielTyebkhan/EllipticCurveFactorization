import sage.all # needed to make sage imports work

import sys
import random
import math
import sage.schemes.elliptic_curves.constructor as EC
import sage.rings.finite_rings.integer_mod_ring as IntModRings

def rand_curve_and_point(n):
    F = IntModRings.IntegerModRing(n)
    A = random.randint(0, n)
    u = random.randint(0, n)
    v = random.randint(0, n)
    C = (v**2 - u**3 - A*u) % n
    curve = EC.EllipticCurve(F, [A, C])
    point = curve([u, v])
    return curve, point


def factor(n):
    searching = True
    B = 10**4   
    fact = math.factorial(B)
    while searching:
        curve, point = rand_curve_and_point(n)
        print(f'Evaluating with {curve} and point: {point}')
        try:
            fact * point
        except ZeroDivisionError as ex:
            failed_inverse = int(ex.args[0].split()[2])
            # print(ex)
            factor1 = math.gcd(failed_inverse, n)
            factor2 = n // factor1
            print(f'Found factorization using gcd({failed_inverse}, {n}) = {factor1} to get {n} = {factor1} * {factor2}')

            searching = False

            
        
    

if __name__ == '__main__':
    default = 6280324898167756003198391309579692155707 * 5301840505616489805533768304463882666999
    factor(default if len(sys.argv) == 1 else int(sys.argv[1]))

