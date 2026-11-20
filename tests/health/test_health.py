"""Unit tests of the runtime plane health shell (stdlib unittest; writes nothing)."""

import importlib
import json
import pathlib
import sys
import threading
import unittest

_SRC = str(pathlib.Path(__file__).resolve().parents[2] / "src")
if sys.path[:1] != [_SRC]:
    sys.path.insert(0, _SRC)

_PACKAGE = "planeon_runtime.health"


def _call(method, path):
    from planeon_runtime.health.app import application

    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    body = b"".join(application({"REQUEST_METHOD": method, "PATH_INFO": path}, start_response))
    return captured["status"], captured["headers"], body


class HealthTest(unittest.TestCase):
    def test_health_mapping_is_closed(self):
        from planeon_runtime.health import health

        self.assertEqual(health(), {"status": "ok", "plane": "runtime"})

    def test_get_health_answers_200_json(self):
        status, headers, body = _call("GET", "/health")
        self.assertEqual(status, "200 OK")
        self.assertEqual(headers["Content-Type"], "application/json")
        self.assertEqual(json.loads(body.decode("utf-8")), {"status": "ok", "plane": "runtime"})

    def test_get_missing_answers_404(self):
        status, _headers, body = _call("GET", "/missing")
        self.assertEqual(status, "404 Not Found")
        self.assertNotIn(b"missing", body)

    def test_post_health_answers_405(self):
        status, _headers, body = _call("POST", "/health")
        self.assertEqual(status, "405 Method Not Allowed")
        self.assertNotIn(b"POST", body)

    def test_import_starts_no_thread(self):
        for name in [n for n in sys.modules if n == "planeon_runtime" or n.startswith("planeon_runtime.")]:
            del sys.modules[name]
        before = threading.active_count()
        importlib.import_module(_PACKAGE)
        self.assertEqual(threading.active_count(), before)


if __name__ == "__main__":
    unittest.main()
