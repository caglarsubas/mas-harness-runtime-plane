"""Health-only shell of the runtime plane.

Importing this package starts no thread, socket, subprocess or listener and
reads no environment variable or file.
"""

from .app import application, health

__all__ = ["application", "health"]
