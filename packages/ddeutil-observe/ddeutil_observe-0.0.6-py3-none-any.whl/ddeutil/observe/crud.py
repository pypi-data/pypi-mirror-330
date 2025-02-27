# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import get_async_session


class BaseCRUD:
    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
    ) -> None:
        self.async_session: AsyncSession = session
