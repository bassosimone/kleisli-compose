"""Base implementation."""

from .mocks import WebPage, dns, fetch


def measure(domain: str) -> WebPage:
    """Measures a single domain name."""
    return fetch(dns(domain))


def measure_list(domains: list[str]) -> list[WebPage]:
    """Measures a list of domain names."""
    result = []
    for domain in domains:
        try:
            result.append(measure(domain))
        except Exception as exc:
            _ = exc  # ignore the exception
    return result
