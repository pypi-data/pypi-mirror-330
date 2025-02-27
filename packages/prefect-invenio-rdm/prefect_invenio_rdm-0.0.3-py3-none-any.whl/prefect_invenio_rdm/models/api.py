"""Custom API response models"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class ErrorType(str, Enum):
    """
    * CREATE: Indicates that an error occurred while creating a deposition.
    * FILE_UPLOAD: Indicates that an error occurred while uploading a file.
    * UPDATE: Indicates that an error occurred while updating a record.
    * PUBLISH: Indicates that an error occurred while publishing a deposition.
    * DELETE: Indicates that an error occured while deleting a deposition.
    """

    CREATE = "create"
    UPDATE = "update"
    FILE_UPLOAD = "file_upload"
    PUBLISH = "publish"
    DELETE = "delete"


class APIError(BaseModel):
    """
    Model to store InvenioRDM API errors.

    Attributes:
        type (ErrorType): An error type.
        error_message (Optional[str]): An error message.
    """

    model_config = ConfigDict(use_enum_values=True)

    type: ErrorType = Field(
        ..., description="The type of error as it relates to the upload process."
    )
    error_message: Optional[str] = Field(None, description="An error message.")


class APIResult(BaseModel):
    """
    Represents the API results of a request.

    Attributes:
        successful (boolean): The success status of the request.
        api_response (Optional[Dict[str, Any]]): The API response.
        error (Optional[APIError]): The error in case of a failure.
    """

    model_config = ConfigDict(use_enum_values=True)

    successful: bool = Field(..., description="The success status of the request.")
    api_response: Optional[Dict[str, Any]] = Field(None, description="An API response.")
    error: Optional[APIError] = Field(None, description="An API error.")
