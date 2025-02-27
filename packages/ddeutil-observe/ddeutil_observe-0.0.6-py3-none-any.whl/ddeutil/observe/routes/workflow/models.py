# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, relationship, selectinload
from sqlalchemy.sql.expression import select
from sqlalchemy.types import (
    JSON,
    Boolean,
    DateTime,
    Integer,
    String,
)
from typing_extensions import Self

from ...db import Base, Col


class Workflows(Base):
    __tablename__ = "workflows"

    id = Col(Integer, primary_key=True, index=True)
    name = Col(String(128), index=True)
    desc = Col(String)
    params: Mapped[dict[str, Any]] = Col(JSON)
    on: Mapped[dict[str, Any]] = Col(JSON)
    jobs: Mapped[dict[str, Any]] = Col(JSON)
    delete_flag = Col(Boolean, default=False)
    valid_start = Col(DateTime)
    valid_end = Col(DateTime)

    releases: Mapped[list[WorkflowReleases]] = relationship(
        "WorkflowReleases",
        back_populates="workflow",
    )

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        include_release: bool = False,
    ) -> AsyncIterator[Self]:
        stmt = select(cls)
        if include_release:
            stmt = stmt.options(selectinload(cls.releases))
        if skip > 0 and limit > 0:
            stmt = stmt.offset(skip).limit(limit)

        async for row in (
            (await session.stream(stmt.order_by(cls.id))).scalars().all()
        ):
            yield row


class WorkflowReleases(Base):
    __tablename__ = "workflow_releases"

    id: Mapped[int] = Col(Integer, primary_key=True, index=True)
    release: Mapped[int] = Col(Integer, index=True)
    workflow_id: Mapped[int] = Col(Integer, ForeignKey("workflows.id"))

    workflow: Mapped[Workflows] = relationship(
        "Workflows", back_populates="releases"
    )
    logs: Mapped[list[WorkflowLogs]] = relationship(
        "WorkflowLogs",
        back_populates="release",
    )


class WorkflowLogs(Base):
    __tablename__ = "workflow_logs"

    run_id: Mapped[str] = Col(String, primary_key=True, index=True)
    context: Mapped[dict] = Col(JSON)
    release_id: Mapped[int] = Col(Integer, ForeignKey("workflow_releases.id"))

    release: Mapped[WorkflowReleases] = relationship(
        "WorkflowReleases",
        back_populates="logs",
    )
