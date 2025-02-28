from abc import ABC, abstractmethod
import logging
from .models import Response
from typing import Optional


class BaseTurnstile(ABC):
    """
    Abstract base class for implementing Cloudflare Turnstile validation.

    This class provides the foundational structure for creating a Turnstile
    validator, including the necessary configuration for secret management
    and idempotency.

    Attributes:
        _secret (str): The Cloudflare Turnstile secret used for validation.
        _validateRoute (str): The URL endpoint for Turnstile validation.
    """

    def __init__(self, secret: str):
        """Initializes the Turnstile client instance with the provided secret.

        Args:
            secret (str): Your Cloudflare Turnstile secret.
        """
        self._secret = secret

        self._validateRoute = (
            "https://challenges.cloudflare.com/turnstile/v0/siteverify"
        )

        self.logger = logging.getLogger("cloudstile")

    @abstractmethod
    def validate(
        self,
        token: str,
        ip: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Response:
        """
        Validates the provided Turnstile token against the Cloudflare
        Turnstile service.

        This method must be implemented by subclasses to perform the actual
        validation logic.

        Args:
            token (str): The Turnstile token to validate.
            ip (Optional[str]): The IP address of the user submitting the
                token. Defaults to None.
            idempotency_key (Optional[str]): A unique key to ensure that
                the validation request is idempotent. Defaults to None.

        Returns:
            Response: The response from the Turnstile validation service,
                which contains the result of the validation.
        """
