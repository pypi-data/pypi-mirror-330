# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
"""
This file will contain script that will run before the app start to create the
super admin user.
"""

from __future__ import annotations

import asyncio

from sqlalchemy import insert, select

from .auth.models.user import User
from .auth.securities import get_password_hash
from .conf import config
from .db import sessionmanager
from .deps import get_async_session
from .utils import get_logger

logger = get_logger("ddeutil.observe")
sessionmanager.init(config.sqlalchemy_db_async_url)


async def create_admin(session) -> None:
    username: str = config.web_admin_user
    email: str = config.web_admin_email
    hashed_password = get_password_hash(config.web_admin_pass)

    # NOTE: Check this user already exists on the current backend database.
    user: User | None = (
        await session.execute(
            select(User).filter(User.username == username).limit(1)
        )
    ).scalar_one_or_none()

    if user is None:
        async with sessionmanager.connect() as conn:
            await conn.execute(
                insert(User).values(
                    {
                        "username": username,
                        "email": email,
                        "hashed_password": hashed_password,
                        "is_superuser": True,
                    }
                )
            )
            await conn.commit()

        logger.info(f"Admin user {username} created successfully.")
    else:
        logger.info(f"Admin user {username} already exists.")


async def main():
    async with get_async_session() as session:
        await create_admin(session)


if __name__ == "__main__":
    # NOTE: Start running create function.
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
