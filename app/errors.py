from typing import Annotated, Any, Dict, Optional

from fastapi import HTTPException
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
    A generic helper function to raise an HTTPException

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
