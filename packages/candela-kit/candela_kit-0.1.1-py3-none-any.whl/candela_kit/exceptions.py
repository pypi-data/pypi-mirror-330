from __future__ import annotations

import json
from json import JSONDecodeError
from typing import Dict

from requests import Response


class CandelaApiError(Exception):

    def __init__(
        self, status_code: int, url: str, method: str, reason: str, details: str | Dict
    ):
        self.status_code = status_code
        self.url = url
        self.method = method
        self.reason = reason
        self.details = details
        super().__init__()

    @classmethod
    def from_requests_response(cls, response: Response) -> CandelaApiError:
        try:
            details = response.json()
        except JSONDecodeError:
            details = response.text
        return CandelaApiError(
            response.status_code,
            response.url,
            response.request.method,
            response.reason,
            details,
        )

    def __str__(self):
        return (
            f"{self.method} {self.url} failed ({self.status_code}: {self.reason})"
            f"\nDetails: {json.dumps(self.details, indent=2)}"
        )
