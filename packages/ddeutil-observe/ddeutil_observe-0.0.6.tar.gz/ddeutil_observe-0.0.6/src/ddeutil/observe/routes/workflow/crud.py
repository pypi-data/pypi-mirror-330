# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from collections.abc import AsyncIterator
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import false

from ...crud import BaseCRUD
from ...utils import get_logger
from . import models as md
from .schemas import ReleaseLogCreate, Workflow, WorkflowCreate

logger = get_logger("ddeutil.observe")


async def get_workflow(
    session: AsyncSession,
    workflow_id: int,
) -> md.Workflows:
    return (
        await session.execute(
            select(md.Workflows).filter(md.Workflows.id == workflow_id).limit(1)
        )
    ).first()


async def get_workflow_by_name(
    session: AsyncSession,
    name: str,
) -> md.Workflows:
    return (
        await session.execute(
            select(md.Workflows)
            .filter(
                md.Workflows.name == name,
                md.Workflows.delete_flag == false(),
            )
            .limit(1)
        )
    ).first()


async def create_workflow(
    session: AsyncSession,
    workflow: WorkflowCreate,
) -> md.Workflows:
    db_workflow = md.Workflows(
        name=workflow.name,
        desc=workflow.desc,
        params=workflow.params,
        on=workflow.on,
        jobs=workflow.jobs,
        valid_start=datetime.now(),
        valid_end=datetime(2999, 12, 31),
    )
    session.add(db_workflow)
    await session.flush()
    await session.commit()
    await session.refresh(db_workflow)
    return db_workflow


async def list_workflows(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 1000,
) -> list[md.Workflows]:
    return (
        (
            await session.execute(
                select(md.Workflows)
                .filter(md.Workflows.delete_flag == false())
                .offset(skip)
                .limit(limit)
            )
        )
        .scalars()
        .all()
    )


async def search_workflow(
    session: AsyncSession,
    search_text: str,
) -> list[md.Workflows]:
    if len(search_text) > 0:
        if not (search_text := search_text.strip().lower()):
            return []

        results = []
        for workflow in await list_workflows(session=session):
            text: str = f"{workflow.name} {workflow.desc or ''}".lower()
            logger.debug(f"Getting text: {text} | Search {search_text}")
            if search_text in text:
                results.append(workflow)
        return results
    return await list_workflows(session=session)


async def get_release(
    session: AsyncSession,
    release: datetime,
) -> md.WorkflowReleases:
    return (
        await session.execute(
            select(md.WorkflowReleases)
            .filter(md.WorkflowReleases.release == release)
            .limit(1)
        )
    ).first()


async def create_release_log(
    session: AsyncSession,
    workflow_id: int,
    release_log: ReleaseLogCreate,
):
    db_release = md.WorkflowReleases(
        release=release_log.release,
        workflow_id=workflow_id,
    )
    session.add(db_release)
    await session.flush()
    await session.commit()
    await session.refresh(db_release)

    for log in release_log.logs:
        db_log = md.WorkflowLogs(
            run_id=log.run_id,
            context=log.context,
            release_id=db_release.id,
        )
        session.add(db_log)
        await session.flush()
        await session.commit()
        await session.refresh(db_log)
    return db_release


async def get_log(session: AsyncSession, run_id: str) -> md.WorkflowLogs:
    return (
        await session.execute(
            select(md.WorkflowLogs)
            .filter(md.WorkflowLogs.run_id == run_id)
            .limit(1)
        )
    ).first()


class WorkflowsCRUD(BaseCRUD):

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> AsyncIterator[Workflow]:
        async for wf in md.Workflows.get_all(
            self.async_session,
            skip=skip,
            limit=limit,
            include_release=True,
        ):
            yield Workflow.model_validate(wf)
