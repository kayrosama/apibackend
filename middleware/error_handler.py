from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from utils.logger import get_logger

logger = get_logger("ApiBackEnd")

async def log_exceptions_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.error(str(exc), exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
