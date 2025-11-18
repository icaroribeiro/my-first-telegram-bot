from typing import TypedDict

from fastapi import HTTPException, status


class AppErrorDetails(TypedDict):
    message: str
    detail: str | None
    is_operational: bool


class AppError(HTTPException):
    def __init__(
        self, message: str, status_code: int | None = None, detail: str | None = None
    ) -> None:
        if status_code is None:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.error_details: AppErrorDetails = {
            "message": message,
            "detail": detail,
            "is_operational": f"{status_code}".startswith("4"),
        }
        super().__init__(status_code=status_code, detail=detail)
