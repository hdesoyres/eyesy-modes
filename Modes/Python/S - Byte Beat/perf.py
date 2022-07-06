import time
import timeit
import numpy as np
import byte_functions

REPEATS = 100
NUMBER = 1

SIZE = 1000000
arr_int64 = np.arange(SIZE)
arr_in8 = np.arange(SIZE).astype('uint8')
arr_float = np.arange(SIZE).astype('uint8') / 3.0


def function():
    # time.sleep(0.001)
    # np.sin(arr_float)
    byte_functions.sin(arr_in8)


def log_perf(function, name):
    results = timeit.Timer(function).repeat(repeat=REPEATS, number=NUMBER)
    mean_time = int(1000 * sum(results) / len(results))
    min_time = int(1000 * min(results))
    max_time = int(1000 * max(results))
    print('Function %s' % name)
    print('Mean: %s, Max: %s, Min: %s' % (mean_time, max_time, min_time))


log_perf(lambda: np.sin(arr_float), 'np.sin(arr_float)')
log_perf(lambda: eval('np.sin(arr_float)'), 'eval(np.sin(arr_float))')
log_perf(lambda: np.sin(arr_in8), 'np.sin(arr_in8)')
# np.sin(arr_int64)
# Mean: 18, Max: 31, Min: 17