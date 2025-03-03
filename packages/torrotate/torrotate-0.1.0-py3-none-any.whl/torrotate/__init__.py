"""
TorRotate: A drop-in replacement for requests that routes through Tor with IP rotation
"""

__version__ = "0.1.0"

from .core import (
    configure,
    rotate_ip,
    get_current_ip,
    reset_rotation_counter,
    force_new_ip,
    configure_tor,
    requests,
)

__all__ = [
    "configure",
    "rotate_ip",
    "get_current_ip",
    "reset_rotation_counter",
    "force_new_ip",
    "configure_tor",
    "requests",
]