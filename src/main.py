from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.core.config import settings
from src.api.endpoints.auth_endpoint import user_router 


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.debug,
    docs_url="/docs",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.cors_origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app", host="127.0.0.1", port=8000, # for docker host is 0.0.0.0
)