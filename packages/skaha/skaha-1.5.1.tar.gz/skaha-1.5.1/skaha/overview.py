"""Skaha Overview."""

import defusedxml.ElementTree as ET
from pydantic import model_validator
from requests.models import Response
from typing_extensions import Self

from skaha.client import SkahaClient
from skaha.utils import logs

log = logs.get_logger(__name__)


class Overview(SkahaClient):
    """Overview of the Skaha Server.

    Args:
        SkahaClient (Object): Skaha Client.
    """

    @model_validator(mode="after")
    def _set_server(self) -> Self:
        """Sets the server path after validation."""
        suffix = "availability"
        self.server = f"{self.server}/{suffix}"  # type: ignore
        log.debug(f"Server set to {self.server}")
        return self

    def availability(self) -> bool:
        """Check if the server backend is available.

        Returns:
            bool: True if the server is available, False otherwise.
        """
        response: Response = self.session.get(url=self.server)  # type: ignore # noqa
        response.raise_for_status()
        # Parse the XML string
        root = ET.fromstring(response.text)
        available = root.find(
            ".//{http://www.ivoa.net/xml/VOSIAvailability/v1.0}available"
        ).text  # type: ignore
        log.info("Server available: %s", available)
        if available == "true":
            return True
        return False
