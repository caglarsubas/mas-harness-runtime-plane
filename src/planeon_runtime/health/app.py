"""Health endpoint of the runtime plane shell (standard library only).

``health()`` returns the closed health mapping. ``application`` is a WSGI
callable: GET /health answers 200 with that mapping as JSON, any other path
answers 404 and any other method on /health answers 405. Responses never echo
the request.
"""

import json

_HEALTH_PATH = "/health"
_JSON = "application/json"


def health():
    """Return the closed health mapping of the runtime plane."""
    return {"status": "ok", "plane": "runtime"}


def _respond(start_response, status, payload, extra_headers=()):
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    headers = [("Content-Type", _JSON), ("Content-Length", str(len(body)))]
    headers.extend(extra_headers)
    start_response(status, headers)
    return [body]


def application(environ, start_response):
    """WSGI callable serving GET /health only."""
    path = environ.get("PATH_INFO", "")
    if path != _HEALTH_PATH:
        return _respond(start_response, "404 Not Found", {"error": "not_found"})
    method = environ.get("REQUEST_METHOD", "")
    if method != "GET":
        return _respond(
            start_response,
            "405 Method Not Allowed",
            {"error": "method_not_allowed"},
            (("Allow", "GET"),),
        )
    return _respond(start_response, "200 OK", health())
