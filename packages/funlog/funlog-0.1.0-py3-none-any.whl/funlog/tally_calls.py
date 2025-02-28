import functools
import threading
import time
from dataclasses import dataclass, replace
from typing import Any, Callable, cast, Dict, Optional, TypeVar

from .log_calls import (
    _func_and_module_name,
    _get_log_func,
    EMOJI_TIMING,
    format_duration,
    LogFunc,
    LogLevelStr,
)


F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class Tally:
    calls: int = 0
    total_time: float = 0.0
    last_logged_count: int = 0
    last_logged_total_time: float = 0.0


_tallies: Dict[str, Tally] = {}
_tallies_lock = threading.Lock()


def tally_calls(
    level: LogLevelStr = "info",
    min_total_runtime: float = 0.0,
    periodic_ratio: float = 2.0,
    if_slower_than: float = float("inf"),
    log_func: Optional[LogFunc] = None,
) -> Callable[[F], F]:
    """
    Decorator to monitor performance by tallying function calls and total runtime, only logging
    periodically (every time calls exceed `periodic_ratio` more in count or runtime than the last
    time it was logged) or if runtime is greater than `if_slower_than` seconds).
    """

    log_func = _get_log_func(level, log_func)

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()

            result = func(*args, **kwargs)

            end_time = time.time()
            elapsed = end_time - start_time

            func_name = _func_and_module_name(func)

            should_log = False
            calls: int = 0
            total_time: float = 0.0

            with _tallies_lock:
                if func_name not in _tallies:
                    _tallies[func_name] = Tally()

                _tallies[func_name].calls += 1
                _tallies[func_name].total_time += elapsed

                should_log = _tallies[func_name].total_time >= min_total_runtime and (
                    elapsed > if_slower_than
                    or _tallies[func_name].calls
                    >= periodic_ratio * _tallies[func_name].last_logged_count
                    or _tallies[func_name].total_time
                    >= periodic_ratio * _tallies[func_name].last_logged_total_time
                )

                if should_log:
                    calls = _tallies[func_name].calls
                    total_time = _tallies[func_name].total_time
                    _tallies[func_name].last_logged_count = calls
                    _tallies[func_name].last_logged_total_time = total_time

            if should_log:
                log_func(
                    "%s %s() took %s, now called %d times, %s avg per call, total time %s",
                    EMOJI_TIMING,
                    func_name,
                    format_duration(elapsed),
                    calls,
                    format_duration(total_time / calls),
                    format_duration(total_time),
                )

            return result

        return cast(F, wrapper)

    return cast(Callable[[F], F], decorator)


def log_tallies(
    level: LogLevelStr = "info",
    if_slower_than: float = 0.0,
    log_func: Optional[LogFunc] = None,
):
    """
    Log all tallies and runtimes of tallied functions.
    """
    log_func = _get_log_func(level, log_func)

    with _tallies_lock:
        tallies_copy = {k: replace(t) for k, t in _tallies.items()}

    tallies_to_log = {
        k: t for k, t in tallies_copy.items() if t.total_time >= if_slower_than
    }
    if tallies_to_log:
        log_lines = []
        log_lines.append(f"{EMOJI_TIMING} Function tallies:")
        for fkey, t in sorted(
            tallies_to_log.items(), key=lambda item: item[1].total_time, reverse=True
        ):
            log_lines.append(
                "    %s() was called %d times, total time %s, avg per call %s"
                % (
                    fkey,
                    t.calls,
                    format_duration(t.total_time),
                    format_duration(t.total_time / t.calls) if t.calls else "N/A",
                )
            )
        log_func("\n".join(log_lines))
