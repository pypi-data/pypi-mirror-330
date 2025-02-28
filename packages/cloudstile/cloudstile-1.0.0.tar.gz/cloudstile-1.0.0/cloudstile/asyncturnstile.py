import json
import traceback
from typing import Optional
from .base import BaseTurnstile
from .models import HTTPError, InvalidInputSecret, Response
import httpx


class AsyncTurnstile(BaseTurnstile):
    """
    Asynchronous implementation of the Cloudflare Turnstile API.

    This class extends the BaseTurnstile class to provide an asynchronous
    method for validating Turnstile tokens using the Cloudflare Turnstile
    service.

    Inherits from:
        BaseTurnstile: The abstract base class for Turnstile validation.
    """

    async def validate(
        self,
        token: str,
        ip: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Response:
        """
        Asynchronously validates the provided Turnstile token against the
        Cloudflare Turnstile service.

        This method sends a POST request to the Turnstile validation endpoint
        with the necessary parameters and returns the validation response.

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
        async with httpx.AsyncClient() as client:

            data = {
                "secret": self._secret,
                "response": token,
            }

            if ip:
                data["remoteip"] = ip

            if idempotency_key:
                data["idempotency_key"] = idempotency_key

            resp = await client.post(self._validateRoute, json=data)
            resp.raise_for_status()

            response = Response.model_validate(resp.json())

            return response
