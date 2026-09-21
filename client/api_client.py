"""Reusable HTTP boundary that provides session management and request telemetry."""

import logging
import time
from typing import Any

import requests
from requests import Response

from config.settings import settings

logger = logging.getLogger(__name__)


class ApiClient:
    """Send JSONPlaceholder requests through one persistent HTTP session."""

    def __init__(self, base_url: str = settings.base_url, timeout: float = settings.timeout):
        """Goal: configure the base URL and timeout for an API test session.

        Assertion: the client stores a normalized URL and a positive request timeout.
        SDET Rationale: centralized connection settings keep suites consistent and make
        environment changes explicit without duplicating HTTP setup in tests.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        # A Session reuses TCP connections, reducing handshake overhead across a suite.
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method: str, path: str, **kwargs: Any) -> Response:
        """Goal: execute one HTTP request for any supported API verb.

        Assertion: log method, status, and elapsed time in milliseconds for observability.
        SDET Rationale: per-request latency telemetry exposes SLA regressions while
        keeping transport behavior in one maintainable wrapper.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        kwargs.setdefault("timeout", self.timeout)
        started_at = time.perf_counter()
        try:
            response = self.session.request(method, url, **kwargs)
        except Exception:
            latency_ms = (time.perf_counter() - started_at) * 1000
            logger.exception("%s %s | Failed | Latency: %.2fms", method.upper(), path, latency_ms)
            raise
        latency_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "%s %s | Status: %s | Latency: %.2fms",
            method.upper(),
            path,
            response.status_code,
            latency_ms,
        )
        return response

    def get(self, path: str, **kwargs: Any) -> Response:
        """Goal: issue a GET request to the supplied resource path.

        Assertion: the response is returned for status, headers, and schema assertions.
        SDET Rationale: a named verb method keeps tests readable while centralizing telemetry.
        """
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> Response:
        """Goal: issue a POST request with the caller's JSON payload.

        Assertion: the response is returned for status, headers, and payload assertions.
        SDET Rationale: the shared wrapper guarantees consistent timing for write operations.
        """
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> Response:
        """Goal: issue a PUT request for full resource replacement.

        Assertion: the response is returned for status, headers, and replacement assertions.
        SDET Rationale: the explicit method maps test intent directly to HTTP semantics.
        """
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> Response:
        """Goal: issue a PATCH request for partial resource updates.

        Assertion: the response is returned for status, headers, and changed-field assertions.
        SDET Rationale: centralized partial-update transport keeps latency measurement uniform.
        """
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> Response:
        """Goal: issue a DELETE request for the supplied resource path.

        Assertion: the response is returned for status and deletion-contract assertions.
        SDET Rationale: consistent DELETE handling makes mock API semantics easy to verify.
        """
        return self.request("DELETE", path, **kwargs)

    @staticmethod
    def assert_status(response: Response, expected: int) -> None:
        """Goal: enforce the expected HTTP status for a test operation.

        Assertion: response status equals the caller's expected status code.
        SDET Rationale: a readable failure preserves response context for rapid diagnosis.
        """
        assert response.status_code == expected, (
            f"Expected HTTP {expected}, got {response.status_code}: {response.text[:500]}"
        )

    def close(self) -> None:
        """Goal: release pooled connections after the test session.

        Assertion: the underlying Session is closed by the fixture teardown.
        SDET Rationale: deterministic cleanup prevents leaked sockets in local and CI runs.
        """
        self.session.close()
