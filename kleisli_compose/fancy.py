"""Fancy monadic implementation of measure_list."""

from __future__ import annotations

from typing import Callable, Iterable

from .full import Compose, dnsx, fetchxy
from .mocks import WebPage


class Func[A, B]:
    """Generic monad-aware function."""

    def __init__(self, fx: Callable[[A], B | Exception]):
        self.fx = fx

    def __call__(self, a: A) -> B | Exception:
        """Monadic function call."""
        return self.fx(a)

    def __or__[C](self, other: Func[B, C]) -> Func[A, C]:
        """Monadic function composition."""
        return Func(Compose(self.fx, other.fx))


dns_func = Func(dnsx)
"""The monadic function for DNS lookup."""

fetch_func = Func(fetchxy)
"""The monadic function for webpage fetch."""


def measure_iter(domains: list[str]) -> Iterable[WebPage | Exception]:
    """Measures a list of domain names."""
    return map(dns_func | fetch_func, domains)


def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    """Measures a list of domain names."""
    return list(measure_iter(domains))
