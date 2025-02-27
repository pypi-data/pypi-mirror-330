"""Skaha Client."""

import logging
from os import R_OK, access, environ
from pathlib import Path
from time import asctime, gmtime
from typing import Annotated, Optional

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    ConfigDict,
    Field,
    FilePath,
    field_validator,
    model_validator,
)
from requests import Session
from typing_extensions import Self

from skaha import __version__
from skaha.models import ContainerRegistry

# Setup logging format
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
# Get the logger
log = logging.getLogger(__name__)


class SkahaClient(BaseModel):
    """Skaha Client.

    Args:
        server (str): Server URL.
        version (str): Skaha API version.
        certificate (str): Certificate file.
        timeout (int): Timeout for requests.
        session (Session): Requests HTTP Session object.
        verify (bool): Verify SSL certificate.
        registry (ContainerRegistry): Credentials for a private registry.

    Raises:
        ValidationError: If the client is misconfigured.

    Examples:
        >>> from skaha.client import SkahaClient

            class Sample(SkahaClient):
                pass
    """

    server: AnyHttpUrl = Field(
        default="https://ws-uv.canfar.net/skaha",
        title="Skaha Server URL",
        description="Location of the Skaha API server.",
    )
    version: str = Field(
        default="v0",
        title="Skaha API Version",
        description="Version of the Skaha API to use.",
    )
    certificate: FilePath = Field(
        default=Path(f"{environ['HOME']}/.ssl/cadcproxy.pem"),
        title="X509 Certificate",
        description="Path to the X509 certificate used for authentication.",
        validate_default=True,
    )
    timeout: int = Field(
        default=15,
        title="HTTP Timeout",
        description="HTTP Timeout in seconds for requests.",
    )
    verify: bool = Field(default=True)
    registry: Annotated[
        Optional[ContainerRegistry],
        Field(
            default=None,
            title="Container Registry",
            description="Credentials for a private container registry.",
        ),
    ] = None
    session: Annotated[
        Session,
        Field(
            default=Session(),
            title="HTTP Requests Session",
            description="HTTP Requests Session.",
        ),
    ] = Session()

    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    @field_validator("certificate")
    @classmethod
    def _check_certificate(cls, value: FilePath) -> FilePath:
        """Validate the certificate file.

        Args:
            value (FilePath): Path to the certificate file.

        Returns:
            FilePath: Validated Path to the certificate file.
        """
        # Check if the certificate is a valid path
        assert (
            Path(value).resolve(strict=True).is_file()
        ), f"{value} is not a file or does not exist."
        assert access(Path(value), R_OK), f"{value} is not readable."
        return value

    @model_validator(mode="after")
    def _create_session(self) -> Self:
        """Update the session object with the HTTP headers.

        Returns:
            Self: Updated SkahaClient object.
        """
        self.session.headers.update({"X-Skaha-Server": str(self.server)})
        self.session.headers.update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )
        self.session.headers.update({"Accept": "*/*"})
        self.session.headers.update({"Date": asctime(gmtime())})
        self.session.headers.update({"X-Skaha-Client": f"python/{__version__}"})
        self.session.headers.update({"X-Skaha-Authentication-Type": "certificate"})
        self.session.cert = str(self.certificate)
        self.session.verify = self.verify
        if self.registry:
            self.session.headers.update(
                {"X-Skaha-Registry-Auth": f"{self.registry.encoded()}"}
            )
        return self
