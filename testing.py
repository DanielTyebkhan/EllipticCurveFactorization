from EllipticCurves import EllipticCurveModN
from Lenstra import factor
from math_helpers import mult_inverse

def main():
    n = 5 * 27
    res = factor(n)
    print(res.success_attempt.factors)
    # curve, point = EllipticCurveModN.rand_curve_and_point_mod_n(670)
    # sum = point
    # for i in range(2, 8):
    #     sum = curve.add_points(point ,sum)
    #     print(f'{i} * {point} = {sum}')

if __name__ == '__main__':
    main()