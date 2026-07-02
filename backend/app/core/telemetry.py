from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
from time import perf_counter
from typing import Iterator

from app.core.logging import logger


class Telemetry:
    def __init__(self) -> None:
        self.counters: Counter[str] = Counter()
        self.timings_ms: Counter[str] = Counter()

    def increment(self, key: str, amount: int = 1) -> None:
        self.counters[key] += amount

    def record_timing(self, key: str, elapsed_ms: int) -> None:
        self.timings_ms[key] += elapsed_ms

    @contextmanager
    def track(self, key: str) -> Iterator[None]:
        start = perf_counter()
        try:
            yield
            self.increment(f"{key}.success")
        except Exception:
            self.increment(f"{key}.error")
            logger.exception("Telemetry tracked error: %s", key)
            raise
        finally:
            elapsed_ms = int((perf_counter() - start) * 1000)
            self.record_timing(f"{key}.time_ms", elapsed_ms)

    def snapshot(self) -> dict[str, dict[str, int]]:
        return {
            "counters": dict(self.counters),
            "timings_ms": dict(self.timings_ms),
        }


telemetry = Telemetry()

