import dataclasses
import datetime
import logging
import os
from enum import Enum, auto, unique
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)


@unique
class ZmSystemEnums(Enum):
    ZIMASAMED = auto()


class ZmDefaultConfig:
    @staticmethod
    def get_var(
        suffix: str,
        zm_sys_enum: Optional[ZmSystemEnums] = None,
        raise_error: bool = True,
    ) -> str:
        if zm_sys_enum:
            key = f"ZBUS_{zm_sys_enum.name}_{suffix}"
        else:
            key = f"ZBUS_{suffix}"
        var = os.getenv(key)
        if raise_error and not var:
            raise ValueError(f"{key} env var not set!")
        return var

    @staticmethod
    def date_encoder(dt: Optional[datetime.date]) -> Optional[str]:
        default_date_format = "%Y-%m-%d"
        if not dt:
            return dt
        DATEFORMAT = (
            ZmDefaultConfig.get_var("DATEFORMAT", None, False) or default_date_format
        )
        return dt.strftime(DATEFORMAT)

    @staticmethod
    def datetime_encoder(dt: Optional[datetime.datetime]) -> Optional[str]:
        default_datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        if not dt:
            return dt
        DATETIMEFORMAT = (
            ZmDefaultConfig.get_var("DATETIMEFORMAT", None, False)
            or default_datetime_format
        )
        return dt.strftime(DATETIMEFORMAT)

    @staticmethod
    def date_decoder(date_string: Optional[str]) -> Optional[datetime.date]:
        default_date_format = "%Y-%m-%d"
        if not date_string:
            return date_string
        DATEFORMAT = (
            ZmDefaultConfig.get_var("DATEFORMAT", None, False) or default_date_format
        )
        return datetime.datetime.strptime(date_string, DATEFORMAT)

    @staticmethod
    def datetime_decoder(date_string: Optional[str]) -> Optional[datetime.datetime]:
        default_datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        if not date_string:
            return date_string
        DATETIMEFORMAT = (
            ZmDefaultConfig.get_var("DATETIMEFORMAT", None, False)
            or default_datetime_format
        )
        return datetime.datetime.strptime(date_string, DATETIMEFORMAT)


@dataclasses.dataclass
class TokenManager:
    auth_url: str
    username: str
    password: str
    client_id: str
    grant_type: str
    __token: str = dataclasses.field(default=None)
    __expires_at: datetime.datetime = dataclasses.field(
        default_factory=datetime.datetime.utcnow
    )

    def generate_token(self) -> None:
        url = self.auth_url
        if not url:
            self.__token = "NO_AUTH_URL"
            self.__expires_at = self.__expires_at + datetime.timedelta(seconds=1000 * 3)
            return
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'grant_type': self.grant_type,
            'client_id': self.client_id,
            'username': self.username,
            'password': self.password
        }
        
        response = requests.post(url=url, headers=headers, data=payload)
        response.raise_for_status()
        body = response.json()
        
        self.__token = body["access_token"]
        expires_in: int = body["expires_in"]
        # using last generated instead of utcnow() to allow room for error
        self.__expires_at = self.__expires_at + datetime.timedelta(
            seconds=expires_in
        )

    def token(self):
        if not self.__token or datetime.datetime.utcnow() >= self.__expires_at:
            self.generate_token()
        return self.__token


@dataclasses.dataclass
class ZmSystem:
    """
    Represents a ZmSystem object that interacts with a ZmSystemEnums instance and a TokenManager instance.

    Attributes:
        zm_system_enum (ZmSystemEnums): The ZmSystemEnums instance representing the type of ZmSystem.
        token_manager (Optional[TokenManager]): The TokenManager instance for managing authentication tokens.

    Methods:
        __post_init__(): Initializes the ZmSystem object and creates a token manager if not already created.
        _get_env_var(suffix: str) -> str: Retrieves an environment variable based on the given suffix.
        base_url() -> str: Returns the base URL for the ZmSystem.
        username() -> str: Returns the username for authentication.
        password() -> str: Returns the password for authentication.
        auth_url() -> str: Returns the authentication URL based on the ZmSystemEnums.
        get_default_headers(authenticated: bool) -> dict: Returns the default headers for API requests.
        request(method: str, url: str, **kwargs) -> Any: Sends an HTTP request with the specified method and URL.

    """

    zm_system_enum: ZmSystemEnums
    token_manager: Optional[TokenManager] = dataclasses.field(default=None)

    def __post_init__(self):
        """
        Initializes the ZmSystem object and creates a token manager if not already created.
        """
        # create token manager if not created
        if not self.token_manager:
            self.token_manager = TokenManager(
                auth_url=self.auth_url, username=self.username, password=self.password, client_id=self.client_id, grant_type=self.grant_type
            )

    def _get_env_var(self, suffix: str) -> str:
        """
        Retrieves an environment variable based on the given suffix.

        Args:
            suffix (str): The suffix of the environment variable.

        Returns:
            str: The value of the environment variable.

        """
        return ZmDefaultConfig.get_var(suffix, self.zm_system_enum)

    @property
    def base_url(self) -> str:
        """
        Returns the base URL for the TqSystem.

        Returns:
            str: The base URL.

        """
        return self._get_env_var("BASEURL")

    @property
    def username(self) -> str:
        """
        Returns the username for authentication.

        Returns:
            str: The username.

        """
        if not self.auth_url:
            return "NO_AUTH_URL"
        return self._get_env_var("USERNAME")

    @property
    def password(self) -> str:
        """
        Returns the password for authentication.

        Returns:
            str: The password.

        """
        if not self.auth_url:
            return "NO_AUTH_URL"
        return self._get_env_var("PASSWORD")

    @property
    def client_id(self) -> str:
        """
        Returns the client ID for authentication.

        Returns:
            str: The client ID.

        """
        return self._get_env_var("CLIENT_ID")

    @property
    def grant_type(self) -> str:
        """
        Returns the grant type for authentication.

        Returns:
            str: The grant type.

        """
        return self._get_env_var("GRANT_TYPE")

    @property
    def auth_url(self) -> str:
        """
        Returns the authentication URL based on the ZmSystemEnums.

        Returns:
            str: The authentication URL.

        """
        verify_url = self._get_env_var("VERIFY_URL")
        return f"{verify_url}realms/zimasa-test/protocol/openid-connect/token"

    def get_default_headers(self, authenticated=True) -> dict:
        """
        Returns the default headers for API requests.

        Args:
            authenticated (bool): Flag indicating whether the request requires authentication.

        Returns:
            dict: The default headers.

        """
        headers = {"Content-Type": "application/json"}
        if not authenticated:
            return headers
        token = self.token_manager.token()
        headers["Authorization"] = f"Bearer {token}"
        return headers

    def request(self, method: str, url: str, **kwargs) -> Any:
        """
        Sends an HTTP request with the specified method and URL.

        Args:
            method (str): The HTTP method for the request.
            url (str): The URL for the request.
            **kwargs: Additional keyword arguments to be passed to the requests library.

        Returns:
            Any: The response data.

        Raises:
            requests.exceptions.RequestException: If the request fails.

        """
        headers = (
            kwargs.get("headers") or self.get_default_headers()
        )  # use passed if any or generate
        kwargs["headers"] = headers  # inject headers
        logger.debug(f"url={url}")
        response = requests.request(method=method, url=url, **kwargs)
        logger.debug(f"response: {response}")
        if response.status_code >= 300:  # inject content to reason
            response.reason = response.reason or response.content
        response.raise_for_status()
        data = response.json()
        logger.debug(f"data={data}")
        return data
