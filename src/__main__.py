from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from api_crud_generate_libary.routers.router import Router

from src.configs.configs import settings
from src.routes import (
    ai_human_sciences_router,
    ai_languages_router,
    ai_math_router,
    ai_natural_sciences_router,
    auth_router,
    question_router,
)
from src.models import routes
from src.middlewares.auth_middleware import jwt_validation

security = HTTPBearer(auto_error=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
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
    question_router,
    tags=["Questions"],
    dependencies=[Depends(security)],
)

for route in routes:
    item = Router(
        model_class=route["model_class"],
        standard_schema=route["standard_schema"],
        db_session=route["db_session"],
        auth_callback=route["auth_callback"],
        request_post_schema=route["request_post_schema"],
        request_patch_schema=route["request_patch_schema"],
        response_get_schema=route["response_get_schema"],
        response_get_by_id_schema=route["response_get_by_id_schema"],
        response_post_schema=route["response_post_schema"],
        response_delete_schema=route["response_delete_schema"],
        response_patch_schema=route["response_patch_schema"],
        use_get=route["use_get"],
        use_get_by_id=route["use_get_by_id"],
        use_post=route["use_post"],
        use_delete=route["use_delete"],
        use_patch=route["use_patch"],
        join_parameters=route["join_parameters"],
        second_level_join_parameters=route["second_level_join_parameters"],
    )

    app.include_router(
        item.router,
        prefix=route["route_prefix"],
        tags=route["route_tags"],
        dependencies=[Depends(security)] if route["dependencies"] else None,
    )

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
