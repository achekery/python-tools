"""functools_ext.py"""

import datetime
import functools
import time

class FunctoolsExt:
    """Namespace for `functools` extensions."""

    @staticmethod
    def stacktracer_fdec_fact(
        sink=print,
        counter=time.perf_counter,
        with_elapsed=False,
    ):
        """Factory for stacktracer function decorator."""

        def _stacktracer_fdec(func):
            """Stacktracer function decorator."""

            @functools.wraps(func)
            def _func(*ar, **kw):
                """Wrapped function for stacktracer function decorator."""
                sink(f">>> {func.__name__} >>> {ar=}; {kw=}")
                time1 = counter()
                try:
                    res = func(*ar, **kw)
                    ela = datetime.timedelta(microseconds=int(1000000*(counter() - time1)))
                    sink(f"<<< {func.__name__} <<< {ela=!s}, {res=!s}")
                    if with_elapsed:
                        return ela, res
                    else:
                        return res
                except Exception as exc:
                    ela = datetime.timedelta(microseconds=int(1000000*(counter() - time1)))
                    sink(f"!!! {func.__name__} !!! {ela=!s}, {exc=!s}")
                    raise

            return _func

        return _stacktracer_fdec

    stacktracer_fdec = stacktracer_fdec_fact()
