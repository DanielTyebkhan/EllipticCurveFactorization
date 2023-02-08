from datetime import datetime

from sage.all import *

import sage.schemes.elliptic_curves.constructor as EC
import sage.rings.finite_rings.integer_mod_ring as IntModRings

import random

from EllipticCurves import EllipticCurveModN

def time_op(op):
    start_time = datetime.now()
    try:
        op()
    except:
        pass
    return (datetime.now() - start_time).microseconds

def main():
    num_curves = 30
    sage_time = 0
    my_time = 0
    num_samples = 1000
    for _ in range(num_curves):
        n = random.randint(100, 10000)
        curve, point = EllipticCurveModN.rand_curve_and_point_mod_n(n)
        a = curve.A
        b = curve.B

        F = IntModRings.IntegerModRing(n)
        sage_curve = EC.EllipticCurve(F, [a, b])
        sage_point = sage_curve([point[0], point[1]])

        samples = random.sample(range(1000000), num_samples)
        
        for s in samples:
            sage_time += time_op(lambda: s * sage_point)
            my_time += time_op(lambda: curve.multiply_point(s, point))
    total_times = num_curves * num_samples
    sage_avg = sage_time / total_times
    my_avg = my_time / total_times
    print(f'Sage avg: {sage_avg}')
    print(f'My avg: {my_avg}')


if __name__ == '__main__':
    main()