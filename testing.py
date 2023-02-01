import random
from EllipticCurves import EllipticCurveModN
import SageLenstra as sl
from Lenstra import run_lenstra_parallel
from math_helpers import mult_inverse


def main():
    random.seed(0)
    n = 2**67 - 1
    # res = sl.run_lenstra_parallel(n, 6, '')
    res = run_lenstra_parallel(n, 6, '')
    print(res.success_attempt.factors)
    # curve, point = EllipticCurveModN.rand_curve_and_point_mod_n(670)
    # sum = point
    # for i in range(2, 8):
    #     sum = curve.add_points(point ,sum)
    #     print(f'{i} * {point} = {sum}')

if __name__ == '__main__':
    main()