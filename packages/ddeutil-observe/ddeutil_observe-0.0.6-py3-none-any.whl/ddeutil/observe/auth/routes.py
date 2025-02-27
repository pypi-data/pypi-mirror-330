# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi import status as st
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..deps import get_async_session
from ..utils import get_logger
from .crud import TokenCRUD, authenticate, verify_refresh_token
from .deps import get_current_active_user, get_current_super_user
from .models import User
from .schemas import (
    TokenCreate,
    TokenRefreshSchema,
    TokenSchema,
    UserSchema,
)
from .securities import (
    create_access_token,
    create_refresh_token,
)

logger = get_logger("ddeutil.observe")
auth = APIRouter(prefix="/auth", tags=["api", "auth"])


@auth.post("/token")
async def token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
    service: TokenCRUD = Depends(TokenCRUD),
) -> TokenRefreshSchema:
    if form_data.grant_type != "password":
        raise HTTPException(
            status_code=st.HTTP_406_NOT_ACCEPTABLE,
            detail=(
                f"grant type: {form_data.grant_type} does not support for this "
                f"application yet."
            ),
        )

    logger.debug("Authentication with user-password")
    user = await authenticate(
        session,
        name=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=st.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    sub: dict[str, Any] = {
        "id": str(user.id),
        "sub": user.username,
        "scopes": form_data.scopes,
    }
    access_token = create_access_token(subject=sub)
    refresh_token = create_refresh_token(subject=sub)
    await service.create(
        token=TokenCreate(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
        ),
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@auth.post("/refresh")
async def refresh(
    grant_type: str = Form(default="refresh_token"),
    refresh_token: str = Form(...),
    scopes: str = Form(default="me"),
    session: AsyncSession = Depends(get_async_session),
) -> TokenSchema:
    if grant_type != "refresh_token":
        raise HTTPException(
            status_code=st.HTTP_404_NOT_FOUND,
            detail="Invalid grant type.",
        )
    if not (user_data := await verify_refresh_token(refresh_token, session)):
        raise HTTPException(
            status_code=st.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token.",
        )
    new_access_token = create_access_token(
        subject={
            "sub": user_data.username,
            "scopes": [s.strip() for s in scopes.split(",")],
        }
    )
    return {"access_token": new_access_token, "token_type": "Bearer"}


@auth.get("/token/me/", response_model=UserSchema)
async def read_token_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Get current active user from the current token."""
    return current_user


@auth.get(
    path="/user/{username}",
    dependencies=[Depends(get_current_super_user)],
)
async def read_user_by_username(
    username: str,
    session: AsyncSession = Depends(get_async_session),
) -> UserSchema:
    return await User.get_by_username(session, username=username)


@auth.get(
    path="/user",
    dependencies=[Depends(get_current_super_user)],
)
async def read_user_all(
    session: AsyncSession = Depends(get_async_session),
) -> list[UserSchema]:
    return await User.get_all(session)
