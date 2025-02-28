from slidge import entrypoint
from slidge.util.util import get_version  # noqa: F401

from . import contact, gateway, session


def main():
    entrypoint("sleamdge")


__all__ = "contact", "gateway", "session", "main"

__version__ = get_version()
