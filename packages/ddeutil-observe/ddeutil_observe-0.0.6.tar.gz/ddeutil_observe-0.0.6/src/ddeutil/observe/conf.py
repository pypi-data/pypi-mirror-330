# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import secrets
from zoneinfo import ZoneInfo

from ddeutil.core import str2bool
from dotenv import load_dotenv

PREFIX: str = "OBSERVE"
ACCESS_DEFAULT: str = secrets.token_urlsafe(32)
REFRESH_DEFAULT: str = secrets.token_urlsafe(32)

# NOTE: Loading environment variable before initialize the FastAPI application.
load_dotenv()


def env(var: str, default: str | None = None) -> str | None:  # pragma: no cov
    return os.getenv(f"{PREFIX}_{var.upper().replace(' ', '_')}", default)


class Config:
    """Base configuration that use on this application on all module that want
    to dynamic value with environment variable changing action.
    """

    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo(env("CORE_TIMEZONE", "UTC"))

    @property
    def api_prefix(self) -> str:
        return env("CORE_API_PREFIX", "/api/v1")

    @property
    def sqlalchemy_db_async_url(self) -> str:
        return env(
            "CORE_SQLALCHEMY_DB_ASYNC_URL",
            "{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
                DB_DRIVER=env("CORE_SQLALCHEMY_DB_DRIVER", "sqlite+aiosqlite"),
                DB_USER=env("CORE_SQLALCHEMY_DB_USER", ""),
                DB_PASSWORD=(
                    f":{pwd}"
                    if (pwd := env("CORE_SQLALCHEMY_DB_PASSWORD"))
                    else ""
                ),
                DB_HOST=env("CORE_SQLALCHEMY_DB_HOST", ""),
                DB_NAME=env("CORE_SQLALCHEMY_DB_NAME", "observe.db"),
            ),
        )

    @property
    def log_debug(self) -> bool:
        return str2bool(env("LOG_DEBUG_MODE", "true"))

    @property
    def log_sqlalchemy_debug(self) -> bool:
        return str2bool(env("LOG_SQLALCHEMY_DEBUG_MODE", "false"))

    @property
    def access_token_expire_mins(self) -> int:
        # NOTE: token: 30 minutes = 30 minutes
        return env("CORE_ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    @property
    def refresh_token_expire_mins(self) -> int:
        # NOTE: refresh: 60 minutes * 24 hours * 8 days  = 8 days
        return env("CORE_REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8)

    @property
    def secret_key(self) -> str:
        # NOTE: Secret keys that use to hash any jwt token generated value.
        return env("CORE_ACCESS_SECRET_KEY", ACCESS_DEFAULT)

    @property
    def refresh_secret_key(self) -> str:
        return env("CORE_REFRESH_SECRET_KEY", REFRESH_DEFAULT)

    @property
    def web_admin_user(self) -> str:
        return env("WEB_ADMIN_USER", "observe")

    @property
    def web_admin_pass(self) -> str:
        return env("WEB_ADMIN_PASS", "observe")

    @property
    def web_admin_email(self) -> str:
        return env("WEB_ADMIN_EMAIL", "observe@mail.com")


config = Config()
