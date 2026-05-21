"""Shared API constraints and route-level exceptions."""

BYPASS_ROUTES = {
    "/",
    "/healthy",
    "/docs",
    "/docs/oauth2-redirect",
    "/openapi.json",
    "/redoc",
    "/register",
    "/login",
    "/forgot-password",
    "/auth/register",
    "/auth/login",
    "/auth/forgot-password",
}
