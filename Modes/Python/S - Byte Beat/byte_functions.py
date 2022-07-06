import numpy as np

BYTES = 512


def _create_cache_1(fn):
    values = np.arange(BYTES) / float(BYTES)
    return fn(values)


def _apply_cache_1(values, cache):
    results = np.zeros(values.shape, dtype=np.uint8)
    results = np.take(cache, values, axis=0, out=results)
    return results


def _apply_cache_2(values_1, values_2, cache):
    results = np.zeros(values_1.shape, dtype=np.uint8)
    results = np.take(cache, values_1, axis=0, out=results)
    return results


float_range = np.arange(BYTES) / float(BYTES)
pi2_range = float_range * 2 * np.pi
sin_cache = (BYTES * (np.sin(pi2_range) + 1) / 2).astype('uint8')


def sin(values):
    return _apply_cache_1(values, sin_cache)


def sqrt(values_1, values_2):
    return _apply_cache_2(values_1, sqrt_cache)


