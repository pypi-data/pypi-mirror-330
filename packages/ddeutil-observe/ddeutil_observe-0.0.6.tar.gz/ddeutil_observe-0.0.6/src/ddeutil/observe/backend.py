# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Callable, Optional

from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthenticationError
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from .auth.crud import verify_refresh_token
from .auth.deps import AnonymousUser, SessionUser, SimpleUser
from .db import sessionmanager


class Backend:
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[tuple[list[str], SessionUser]]:
        raise NotImplementedError()  # pragma: no cover


class OAuth2Backend(Backend):
    """OAuth2 Backend"""

    async def authenticate(
        self,
        conn: HTTPConnection,
    ) -> tuple[list[str], SessionUser]:
        """The authenticate method is invoked each time a route is called that
        the middleware is applied to.

        :param conn: An HTTP connection of FastAPI/Starlette
        :type conn: HTTPConnection

        :rtype: tuple[AuthCredentials, SessionUser]
        :return: A tuple of AuthCredentials (scopes) and a user object that is
            or inherits from BaseUser.
        """
        authorization: Optional[str] = conn.cookies.get("refresh_token")
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            token = None

        # Note: If token does not valid, it will return anonymous user.
        async with sessionmanager.session() as session:
            if (
                token_data := await verify_refresh_token(token, session)
            ) is None:
                return [], AnonymousUser()

        return (
            token_data.scopes,
            SimpleUser(token_data.username),
        )


class OAuth2Middleware:
    def __init__(
        self,
        app: ASGIApp,
        backend: Backend,
        on_error: (
            Callable[[HTTPConnection, AuthenticationError], Response] | None
        ) = None,
    ) -> None:
        self.app = app
        self.backend = backend
        self.on_error: Callable[
            [HTTPConnection, AuthenticationError],
            Response,
        ] = (
            on_error if on_error is not None else self.default_on_error
        )

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
    ) -> None:
        if scope["type"] not in ["http", "websocket"]:
            await self.app(scope, receive, send)
            return

        conn = HTTPConnection(scope)
        try:
            auth_result = await self.backend.authenticate(conn)
        except AuthenticationError as exc:
            response = self.on_error(conn, exc)
            if scope["type"] == "websocket":
                await send({"type": "websocket.close", "code": 1000})
            else:
                await response(scope, receive, send)
            return

        scope["auth"], scope["user"] = auth_result
        await self.app(scope, receive, send)

    @staticmethod
    def default_on_error(_: HTTPConnection, exc: Exception) -> Response:
        return PlainTextResponse(str(exc), status_code=400)
