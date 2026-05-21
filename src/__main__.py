from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware

from src.routes import (
    ai_human_sciences_router,
    ai_languages_router,
    ai_math_router,
    ai_natural_sciences_router,
    auth_router,
)
from src.middlewares.auth_middleware import jwt_validation

security = HTTPBearer(auto_error=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(jwt_validation)


@app.get("/healthy", tags=["Health"])
def healthy():
    """Healthy check route"""
    return {"status": "Ok"}


app.include_router(auth_router, tags=["Authentication"])

app.include_router(
    ai_math_router,
    prefix="/ai",
    tags=["Math Questions"],
    dependencies=[Depends(security)],
)
app.include_router(
    ai_languages_router,
    prefix="/ai",
    tags=["Languages Questions"],
    dependencies=[Depends(security)],
)
app.include_router(
    ai_natural_sciences_router,
    prefix="/ai",
    tags=["Natural Sciences Questions"],
    dependencies=[Depends(security)],
)
app.include_router(
    ai_human_sciences_router,
    prefix="/ai",
    tags=["Human Sciences Questions"],
    dependencies=[Depends(security)],
)
