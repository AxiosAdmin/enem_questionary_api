from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import (
    ai_human_sciences_router,
    ai_languages_router,
    ai_math_router,
    ai_natural_sciences_router,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthy", tags=["Health"])
def healthy():
    """Healthy check route"""
    return {"status": "Ok"}


app.include_router(ai_math_router, prefix="/ai", tags=["Math Questions"])
app.include_router(ai_languages_router, prefix="/ai", tags=["Languages Questions"])
app.include_router(
    ai_natural_sciences_router,
    prefix="/ai",
    tags=["Natural Sciences Questions"],
)
app.include_router(
    ai_human_sciences_router,
    prefix="/ai",
    tags=["Human Sciences Questions"],
)
