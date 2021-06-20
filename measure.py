# The contents of this file is free and unencumbered software released into the
# public domain. For more information, please refer to <http://unlicense.org/>

import time as t
import gc
import pickle


def time(f=None, /, *, repeats=1000000, copy=False, gc_off=True):
    """Performs function time measurement.
    Arguments:
        f: Function to be decorated.
        repeats: How many time 'f' should be run. It's assumed more repeats lead to more accurate results.
        copy: Should 'f' work on copies of the arguments? It's useful when 'f' handles referenced objects - in this case,
            'copy=True' will set copies of original objects as arguments and guarantee that 'f' works on the same data each run.
            'copy=True' leads to slight performance overhead, so if you are sure 'f' will work on the same data,
            set it to 'False'.
        gc_off: If True, this function turns garbage collector off. However, False could be useful in case one measures time in
            'real_life' scenario (when GC is normally on).
    Returns:
        Time elapsed in seconds. Divide by 'repeats' in order to get average.
    """
    def dec_wrapper(f):
        def wrapper(*args, **kwargs):
            # These args and kwargs are wrapped function params
            if gc_off:
                gc_is_enabled = gc.isenabled()
                gc.disable()
            try:
                if copy:
                    elapsed = 0
                    args, kwargs = pickle.dumps(args), pickle.dumps(kwargs)
                    for _ in range(repeats):
                        a, kw = pickle.loads(args), pickle.loads(kwargs)
                        start = t.perf_counter()
                        f(*a, **kw)
                        elapsed += t.perf_counter() - start
                else:
                    start = t.perf_counter()
                    for _ in range(repeats):
                        f(*args, **kwargs)
                    elapsed = t.perf_counter() - start
            finally:
                if gc_off and gc_is_enabled:
                    gc.enable()
            return elapsed
        return wrapper

    if f is None:  # Seems called with parentheses.
        return dec_wrapper
    return dec_wrapper(f)  # Seems called as a plain decorator.
