"""Improves catcher by using avoiding try-catch in measure_list."""

from .mocks import WebPage, dns, fetch


def measure(domain: str) -> WebPage | Exception:
    """Measures a single domain name."""
    try:
        addr = dns(domain)
    except Exception as exc:
        return exc

    try:
        return fetch(addr)
    except Exception as exc:
        return exc


def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    """Measures a list of domain names."""
    result: list[WebPage | Exception] = []
    for domain in domains:
        result.append(measure(domain))
    return result
