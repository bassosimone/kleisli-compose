"""Mocked functions used across this package."""

from dataclasses import dataclass


@dataclass(frozen=True)
class IpAddr:
    """A resolved IP address."""

    address: str


class DNSError(Exception):
    """Error raised when the DNS fails."""


def dns(domain: str) -> IpAddr:
    """Resolve a domain name to a single IP address."""
    if domain != "www.example.com":
        raise DNSError("no such host")
    return IpAddr("130.192.91.211")


@dataclass(frozen=True)
class WebPage:
    """A web page that has been downloaded."""

    page: str


class FetchError(Exception):
    """Error fetching a webpage."""


def fetch(addr: IpAddr) -> WebPage:
    """Fetch a webpage given the IP address."""
    if addr.address != "130.192.91.211":
        raise FetchError("connection reset by peer")
    return WebPage("<html> ...")
