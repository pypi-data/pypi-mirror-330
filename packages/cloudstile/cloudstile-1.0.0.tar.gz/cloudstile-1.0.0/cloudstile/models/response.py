from datetime import datetime
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field


class MetaData(BaseModel):
    """
    Represents metadata associated with the Turnstile response.

    Attributes:
        ephemeral_id (Optional[str]): An optional identifier for the ephemeral session.
    """

    ephemeral_id: Optional[str] = None

    result_with_testing_key: bool = False


class Response(BaseModel):
    """
    Represents the response from the Cloudflare Turnstile verification.

    Attributes:
        success (bool): Indicates whether the verification was successful.
        hostname (str): The hostname of the site where the Turnstile was used.
        action (Optional[str]): An optional action name associated with the Turnstile request.
        cdata (Optional[str]): An optional custom data field, type is set as str for now.
        metadata (Optional[MetaData]): Optional metadata related to the Turnstile response.
        timestamp (datetime): The timestamp of the challenge (alias for 'challenge_ts').
        error_codes (list[Literal]): A list of error codes that may be returned in case of failure.
            Possible values include:
                - "missing-input-secret": The secret parameter is missing.
                - "invalid-input-secret": The secret parameter is invalid.
                - "missing-input-response": The response parameter is missing.
                - "invalid-input-response": The response parameter is invalid.
                - "bad-request": The request is malformed.
                - "timeout-or-duplicate": The request timed out or is a duplicate.
                - "internal-error": An internal error occurred.
    """

    success: bool
    """Indicates whether the verification was successful."""

    hostname: Optional[str] = None
    """The hostname of the site where the Turnstile was used."""

    action: Optional[str] = None
    """An optional action name associated with the Turnstile request."""

    cdata: Optional[str] = (
        None  # I'm unaware of the type Cloudflare uses for this, so I'm setting it as a `str` for now.
    )
    """An optional custom data field.
    
    ---

    *NOTE:* We currently use the `str` type altough this may change if we get clarification on what type Cloudflare returns.
    """

    metadata: MetaData = MetaData()
    """Optional metadata related to the Turnstile response."""

    timestamp: Optional[datetime] = Field(alias="challenge_ts", default=None)
    """The time when the challenge was solved."""

    error_codes: list[str] = Field(validation_alias="error-codes", default_factory=list)
    """A list of error codes that may be returned in case of failure.
    
    - "missing-input-response"
    - "invalid-input-response"
    - "bad-request"
    - "timeout-or-duplicate"
    - "internal-error"
    """
