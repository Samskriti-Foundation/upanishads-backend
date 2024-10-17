from typing import Annotated, Any, Dict, Optional

from fastapi import HTTPException, status
from typing_extensions import Doc


def error_response(
    status_code: Annotated[
        int,
        Doc(
            """
            HTTP status code to send to the client.
            """
        ),
    ],
    detail: Annotated[
        Any,
        Doc(
            """
            Any data to be sent to the client in the `detail` key of the JSON
            response.
            """
        ),
    ] = None,
    headers: Annotated[
        Optional[Dict[str, str]],
        Doc(
            """
            Any headers to send to the client in the response.
            """
        ),
    ] = None,
) -> None:
    """
    A generic helper function to raise an HTTPException.

    Parameters:
        status_code (int): HTTP status code to send to the client.
        detail (Any, optional): Additional data to include in the 'detail' key of the
            JSON response. Defaults to None.
        headers (dict[str, str], optional): Additional headers to send in the response.
            Defaults to None.

    Raises:
        HTTPException: The exception is raised with the specified status code, detail,
            and headers.
    """
    raise HTTPException(status_code=status_code, detail=detail, headers=headers)


def server_error_response(
    error: Annotated[
        Any,
        Doc(
            """
            Error detail to be included in the 500 Internal Server Error response.
            """
        ),
    ]
) -> None:
    """
    Helper function to raise a 500 Internal Server Error response.
    """
    error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": error}
    )


def not_found_error_response():
    """
    Helper function to raise a 404 Not Found error response.
    """
    message = "The requested resource was not found."
    error_response(status_code=status.HTTP_404_NOT_FOUND, detail={"message": message})


def method_not_allowed_error_response():
    """
    Helper function to raise a 405 Method Not Allowed error response.
    """
    message = "The HTTP method used is not allowed for this endpoint."
    error_response(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail={"message": message}
    )


def conflict_error_response(detail: Optional[str] = None) -> None:
    """
    Helper function to raise a 409 Conflict error response.
    """
    message = (
        detail
        or "The request could not be completed because the resource already exists."
    )
    error_response(status_code=status.HTTP_409_CONFLICT, detail={"message": message})
