"""Improves base by catching and reporting exceptions."""

from .base import measure
from .mocks import WebPage


def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    """Measures a list of domain names."""
    result = []
    for domain in domains:
        try:
            result.append(measure(domain))
        except Exception as exc:
            result.append(exc)
    return result
