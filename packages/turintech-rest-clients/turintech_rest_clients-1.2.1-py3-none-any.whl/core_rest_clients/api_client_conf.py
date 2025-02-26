# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from typing import Dict, Optional

from pydantic.v1 import Field, validator

# Internal libraries
from core_common_configuration import BaseConfEnv, conf_factory
from core_utils import url_utils
from core_utils.data_utils import join_values

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["ApiClientConf", "api_client_conf_factory"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                 Configuration class                                                  #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class ApiClientConf(BaseConfEnv):
    """
    This is a configuration class for the API client, primarily used for Rocket Client.
    """

    host: str = Field(
        "127.0.0.1",
        description="The IP address or hostname of the API server to connect to.",
    )
    protocol: str = Field("http", description="Set the HTTP protocol implementation (HTTP, HTTPs)")
    port: Optional[int] = Field(5000, description="The port number to connect to on the API server.")
    postfix: Optional[str] = Field("", description="The postfix to be added to the URL.")
    headers: Optional[Dict[str, str]] = Field(None, description="The headers to be sent.")

    # --------------------------------------------------------------------------------------------------

    @validator("protocol")
    def protocol_validation(cls, value: str) -> str:  # pylint: disable=no-self-argument
        """
        Validate the protocol value.
        """
        _value = value.lower() if value else None
        return _value if _value in ["http", "https"] else "http"

    _validate_no_leading_slash = validator("host", allow_reuse=True)(url_utils.no_leading_slash)
    _validate_no_trailing_slash = validator("host", allow_reuse=True)(url_utils.no_trailing_slash)
    _validate_no_http = validator("host", allow_reuse=True)(url_utils.no_http)

    @property
    def server_url(self):
        """
        Base URL:
            <api_protocol>://<api_host>:<api_port><postfix>
        For rocket client use
        """
        if self.host:
            return join_values(
                values=[
                    f"{self.protocol}://" if self.protocol else None,
                    self.host,
                    f":{self.port}" if self.port else None,
                    f"{self.postfix}" if self.postfix else None,
                ]
            )
        return ""


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Configuration Factory                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def api_client_conf_factory(
    _env_file: Optional[str] = None, prefix: Optional[str] = None, defaults: Optional[Dict] = None, **kwargs
) -> ApiClientConf:
    """This is a factory generating a BasicServerConf class specific to a service, loading every value from a generic
    .env file storing variables in uppercase with a service prefix.

    For rocket client use

    """
    return conf_factory(config_class=ApiClientConf, _env_file=_env_file, prefix=prefix, defaults=defaults, **kwargs)
