"""
oocone.

Unofficial library for interacting with an enocoo energy management system
:author: Simon Leiner <simon@leiner.me>
:license: ISC
"""

from .auth import Auth
from .enocoo import Enocoo

__all__ = ["Auth", "Enocoo"]
