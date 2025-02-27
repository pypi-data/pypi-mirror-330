"""Get available resources from the skaha server."""

from typing import Any, Dict

from pydantic import model_validator
from requests.models import Response
from typing_extensions import Self

from skaha.client import SkahaClient


class Context(SkahaClient):
    """Get available resources from the skaha server."""

    @model_validator(mode="after")
    def _set_server(self) -> Self:
        """Sets the server path after validation."""
        self.server = f"{self.server}/{self.version}/context"  # type: ignore
        return self

    def resources(self) -> Dict[str, Any]:
        """Get available resources from the skaha server.

        Returns:
            A dictionary of available resources.

        Examples:
            >>> from skaha.context import Context
            >>> context = Context()
            >>> context.resources()
            {'cores': {
              'default': 1,
              'defaultRequest': 1,
              'defaultLimit': 16,
              'defaultHeadless': 1,
              'options': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
              },
             'memoryGB': {
              'default': 2,
              'defaultRequest': 4,
              'defaultLimit': 192,
              'defaultHeadless': 4,
              'options': [1,2,4...192]
             },
            'gpus': {
             'options': [1,2, ... 28]
             }
            }
        """
        response: Response = self.session.get(url=self.server)  # type: ignore
        response.raise_for_status()
        return response.json()
