import csv
import os
import Lenstra

def main():
    BENCHMARK_PATH = 'benchmarks.csv'
    benchmarks = csv.DictReader(open(BENCHMARK_PATH))
    for b in benchmarks:
        p = int(b['p'])
        q = int(b['q'])
        name = b['name']
        path = os.path.join('results', name)
        os.makedirs(path)
        Lenstra.run_lenstra_parallel(p*q, 8, path)

if __name__ == '__main__':
    main()