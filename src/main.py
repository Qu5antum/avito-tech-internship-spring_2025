from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from src.core.logging import setup_logging
from src.exception_handlers.base_exception import BaseAppException
from src.core.config import settings
from src.api.endpoints.auth_endpoint import user_router
from src.api.endpoints.pvz_endpoint import pvz_router
from src.api.endpoints.pvz_reception_endpoint import reception_router
from src.api.endpoints.product_endpoint import product_router
from src.middleware.logging_middleware import logging_middleware

setup_logging()
logger = logging.getLogger("errors")

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.debug,
    docs_url="/docs",
)

app.middleware("http")(logging_middleware)


@app.exception_handler(BaseAppException)
async def app_exception_handler(request, exc):
    logger.error(
        "Unhandled exception",
        exc_info=True,
        extra={"path": request.url.path}
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


app.include_router(user_router)
app.include_router(pvz_router)
app.include_router(reception_router)
app.include_router(product_router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", host="127.0.0.1", port=8000, reload=True # for docker host is 0.0.0.0 and not relaod include
)