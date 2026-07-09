"""
Minimal systemd sd_notify client - lets the process report readiness and
periodic "still alive" watchdog pings to systemd, without any extra
dependency (just the raw sd_notify Unix datagram protocol).

Safely does nothing when not running under systemd (e.g. local dev),
since NOTIFY_SOCKET is only set when systemd's Type=notify launched us.
"""

import os
import socket


def _notify(message: str) -> None:
    socket_path = os.environ.get("NOTIFY_SOCKET")

    if not socket_path:
        return

    if socket_path.startswith("@"):
        socket_path = "\0" + socket_path[1:]

    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.connect(socket_path)
        sock.sendall(message.encode("utf-8"))
        sock.close()
    except OSError:
        pass


def notify_ready() -> None:
    """Tell systemd startup is complete - only meaningful with Type=notify."""
    _notify("READY=1")


def notify_watchdog() -> None:
    """
    Pet the watchdog. Call this regularly (well under WatchdogSec) while
    the bot's event loop is healthy - if these stop arriving, systemd
    considers the process hung and force-restarts it.
    """
    _notify("WATCHDOG=1")
