from dataclasses import dataclass
from datetime import datetime
import multiprocessing as mp
import os
from time import time
from typing import Callable, List, Optional, Tuple

import sys
import random
import math
from EllipticCurves import POINT_AT_INFIITY, EllipticCurveModN

from io_helpers import pickle_obj

@dataclass
class LenstraAttempt:
    start_time: datetime
    end_time: datetime
    success: bool
    curve: EllipticCurveModN
    point: List[int]
    max_value_checked: int
    number: int
    factors: Tuple[int, int]


@dataclass
class LenstraResult:
    number: int
    start_time: datetime
    end_time: datetime
    success_attempt: Optional[LenstraAttempt]
    failed_attempts: List[LenstraAttempt]
    
    def is_success(self):
        return self.success_attempt is not None

    def get_total_time(self):
        return self.end_time - self.start_time

    def merge_results(number, results):
        merged = LenstraResult(number=number, start_time=datetime.now(), end_time=datetime.now(), success_attempt=None, failed_attempts=[])
        for r in results:
            if r.is_success():
                merged.success_attempt = r.success_attempt
            merged.failed_attempts += r.failed_attempts
        return merged


def __save_checkpoint(curve, point, b, id, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pickle_obj({'curve': curve, 'point': point, 'time': datetime.now(), 'b': b}, os.path.join(output_dir, str(b) + '.p'))


def factor(n: int, is_cancelled: Callable[[], bool]=lambda: False, proc_id=-1, output_dir=None) -> LenstraResult:
    saving_output = output_dir is not None
    if saving_output:
        proc_out_dir = os.path.join(output_dir, str(proc_id))
    result = LenstraResult(number=n, success_attempt=None, failed_attempts=[], start_time=datetime.now(), end_time=None)
    searching = True
    B = 10**8   
    b = 2
    while searching and not is_cancelled():
        curve, point = EllipticCurveModN.rand_curve_and_point_mod_n(n)
        print(f'Proc {proc_id} Attempting to factor {n} with curve: {curve} and point: {point}')
        start_time = datetime.now()
        prod = point
        while searching and b < B and not is_cancelled():
            if b % 10_000 == 0:
                print(f'Proc {proc_id} at attempt {b}')
                if saving_output:
                    __save_checkpoint(curve, point, b, proc_id, proc_out_dir)
            prod = curve.multiply_point(b, prod)
            if prod == POINT_AT_INFIITY:
                break
            if isinstance(prod, int):
                factor1 = math.gcd(prod, n)
                factor2 = n // factor1
                searching = False
            b += 1
        end_time = datetime.now()
        factors = None if searching else (factor1, factor2)
        success = not searching
        attempt = LenstraAttempt(
            success=success, curve=curve, point=point, number=n, factors=factors, 
            max_value_checked=b, start_time=start_time, end_time=end_time
        )
        if success:
            result.success_attempt = attempt
        else:
            result.failed_attempts.append(attempt)
    result.end_time = datetime.now()
    return result


def factor_for_queue(n: int, queue: mp.Queue, cancel_event: mp.Event, proc_id: int, output_dir: os.PathLike):
    queue.put(factor(n, cancel_event.is_set, proc_id, output_dir))


def run_lenstra_parallel(n: int, num_threads: int, output_path: os.PathLike) -> LenstraResult:
    cancel_event = mp.Event()
    queue = mp.Queue()
    start_time = datetime.now()
    output_dir = os.path.join(output_path, str(start_time))
    procs = [mp.Process(target=factor_for_queue, args=[n, queue, cancel_event, i, output_dir]) for i in range(num_threads)]
    print(f'Starting factorization at {start_time}')
    for p in procs:
        p.start()
    results = [queue.get()]
    end_time = datetime.now()
    print(f'Finished factorization at {end_time}')
    cancel_event.set()
    for _ in range(num_threads - 1):
        results.append(queue.get())
    final_results = LenstraResult.merge_results(n, results)
    final_results.start_time = start_time
    final_results.end_time = end_time
    final_result_path = os.path.join(output_path, 'results.p')
    pickle_obj(final_results, final_result_path)
    factors = final_results.success_attempt.factors
    print(f'Factored: {final_results.number} as {factors[0]} * {factors[1]} in {final_results.get_total_time()}')
    return final_results



def main():
    default = 6280324898167756003198391309579692155707 * 5301840505616489805533768304463882666999
    # default = 7349 * 5281
    number = default if len(sys.argv) == 1 else int(sys.argv[1])
    # print(f'Starting at {start_time}')
    res = run_lenstra_parallel(number, 4, 'results')
    factors = res.success_attempt.factors
    # end_time = datetime.now()
    # print(f'Ending at {end_time}')
    # print(f'Total Time: {end_time - start_time}')


if __name__ == '__main__':
    main()

