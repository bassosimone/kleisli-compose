"""Fully monadic implementation of measure_list."""

from typing import Callable

from .mocks import IpAddr, WebPage, dns, fetch


class Compose[A, B, C]:
    """Implements monadic function composition."""

    def __init__(
        self,
        fx: Callable[[A], B | Exception],
        gx: Callable[[B], C | Exception],
    ):
        self.fx, self.gx = fx, gx

    def __call__(self, a: A) -> C | Exception:
        """Monadic function call."""
        rv = self.fx(a)
        if isinstance(rv, Exception):
            return rv
        return self.gx(rv)


def dnsx(domain: str) -> IpAddr | Exception:
    """Monadic domain name lookup primitive."""
    try:
        return dns(domain)
    except Exception as exc:
        return exc


def fetchxy(addr: IpAddr) -> WebPage | Exception:
    """Monadic webpage fetch primitive."""
    try:
        return fetch(addr)
    except Exception as exc:
        return exc


def measure(domain: str) -> WebPage | Exception:
    """Measures a single domain name."""
    pipeline = Compose(dnsx, fetchxy)
    return pipeline(domain)


def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    """Measures a list of domain names."""
    result: list[WebPage | Exception] = []
    for domain in domains:
        result.append(measure(domain))
    return result
