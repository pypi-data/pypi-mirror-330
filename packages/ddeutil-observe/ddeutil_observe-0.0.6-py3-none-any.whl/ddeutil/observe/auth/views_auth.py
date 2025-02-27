# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Annotated, Union

from fastapi import APIRouter, Depends, Form, Request
from fastapi import status as st
from fastapi.responses import HTMLResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ..conf import config
from ..deps import get_async_session, get_templates
from .crud import TokenCRUD, UserCRUD, authenticate
from .deps import required_current_active_user
from .models import Token, User
from .schemas import (
    PlainTokenSchema,
    TokenCreate,
    UserCreateForm,
    UserResetPassForm,
    UserSchema,
    UserScopeForm,
)
from .securities import create_access_token, create_refresh_token

auth = APIRouter(
    prefix="/auth",
    tags=["auth", "frontend"],
)


@auth.get("/register")
async def register(
    request: Request,
    template: Jinja2Templates = Depends(get_templates),
) -> HTMLResponse:
    return template.TemplateResponse(
        request=request,
        name="auth/authenticate.html",
        context={
            "content": "register",
        },
    )


@auth.post("/register")
async def register_create(
    response: Response,
    form_user: Annotated[UserCreateForm, Form()],
    service: UserCRUD = Depends(UserCRUD),
    token_service: TokenCRUD = Depends(TokenCRUD),
):
    """Register information of user to this application for able to access any
    routes.
    """
    user: UserSchema = await service.create_by_form(form_user)
    await create_login_session(response, token_service, user, scopes=["me"])

    response.headers["HX-Redirect"] = "/"
    response.status_code = st.HTTP_307_TEMPORARY_REDIRECT
    return {}


@auth.get("/login")
async def login(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="auth/authenticate.html",
        context={"content": "login"},
    )


async def create_login_session(
    response: Response,
    service: TokenCRUD,
    user: User | UserSchema,
    scopes: list[str],
) -> Token:
    # NOTE: OAuth2 with scopes such as `["me", ...]`.
    access_token = create_access_token(
        subject={
            "sub": user.username,
            "scopes": scopes,
        },
    )
    refresh_token = create_refresh_token(
        subject={
            "sub": user.username,
            "scopes": scopes,
        },
    )

    # NOTE: Create token on the backend database.
    token: Token = await service.create(
        TokenCreate(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
        )
    )

    # NOTE: Set cookies for refresh tokens.
    response.set_cookie(
        key="refresh_token",
        value=f"Bearer {refresh_token}",
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=config.refresh_token_expire_mins * 60,
    )
    return token


@auth.post("/login")
async def login_create(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    form_scopes: UserScopeForm = Depends(UserScopeForm.as_form),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    service: TokenCRUD = Depends(TokenCRUD),
):
    user: Union[User, bool] = await authenticate(
        session,
        name=form_data.username,
        password=form_data.password,
    )
    if not user:
        response.headers["HX-Redirect"] = "/auth/register"
        response.status_code = st.HTTP_404_NOT_FOUND
        return {}

    token: Token = await create_login_session(
        response, service, user, scopes=form_scopes.scopes
    )

    response.headers["HX-Redirect"] = "/"
    response.status_code = st.HTTP_302_FOUND
    return {
        "access_token": token.token,
        "exp": config.access_token_expire_mins * 60,
        "token_type": "Bearer",
    }


@auth.get("/change-password")
async def change_password(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="auth/authenticate.html",
        context={"request": request, "content": "change-password"},
    )


@auth.post("/change-password")
async def change_password_create(
    response: Response,
    form_data: Annotated[UserResetPassForm, Depends()],
    service: UserCRUD = Depends(UserCRUD),
):
    await service.change_password(form_data)

    response.headers["HX-Redirect"] = "/auth/login"
    response.status_code = st.HTTP_307_TEMPORARY_REDIRECT
    return {"message": "Password changed successfully"}


@auth.post("/logout")
async def logout(
    request: Request,
    response: Response,
    user: User = Depends(required_current_active_user),
    service: TokenCRUD = Depends(TokenCRUD),
):
    await service.retention_by_user(user.id)

    db_tokens: list[Token] = []
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        db_tokens: list[Token] = await service.update_logout(refresh_token)

    # NOTE: Delete cookies for access token and refresh token.
    response.delete_cookie(key="refresh_token", httponly=True)

    response.headers["HX-Redirect"] = "/"
    response.status_code = st.HTTP_302_FOUND
    return {
        "message": "Logout Successfully",
        "logout": [
            PlainTokenSchema.model_validate({"token": token.token}).model_dump()
            for token in db_tokens
        ],
    }
