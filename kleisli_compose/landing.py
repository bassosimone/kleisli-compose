"""Improves bettercatcher by further refactoring the code."""

from .mocks import IpAddr, WebPage, dns, fetch


def dnsx(domain: str) -> IpAddr | Exception:
    """Extend mocks.dns and provide a monad-ready interface."""
    try:
        return dns(domain)
    except Exception as exc:
        return exc


def fetchxy(addr: IpAddr) -> WebPage | Exception:
    """Extend mocks.fetch and provide a monad-ready interface."""
    try:
        return fetch(addr)
    except Exception as exc:
        return exc


def fetchx(addr: IpAddr | Exception) -> WebPage | Exception:
    """Adapt fetchxy type to measure requirements."""
    if isinstance(addr, Exception):
        return addr
    return fetchxy(addr)


def measure(domain: str) -> WebPage | Exception:
    """Measures a single domain name."""
    return fetchx(dnsx(domain))


def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    """Measures a list of domain names."""
    result: list[WebPage | Exception] = []
    for domain in domains:
        result.append(measure(domain))
    return result
