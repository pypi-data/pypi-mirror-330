# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status as st
from sqlalchemy.ext.asyncio import AsyncSession

from ...deps import get_async_session
from .crud import (
    WorkflowsCRUD,
    create_release_log,
    create_workflow,
    get_workflow_by_name,
)
from .schemas import ReleaseLog, ReleaseLogCreate, Workflow, WorkflowCreate

workflow = APIRouter(
    prefix="/workflow",
    tags=["api", "workflow"],
    responses={st.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@workflow.get("/", response_model=list[Workflow])
async def read_all(
    skip: int = 0,
    limit: int = 100,
    service: WorkflowsCRUD = Depends(WorkflowsCRUD),
):
    return [wf async for wf in service.get_all(skip=skip, limit=limit)]


@workflow.post("/", response_model=Workflow)
async def create_workflow(
    wf: WorkflowCreate,
    session: AsyncSession = Depends(get_async_session),
):
    db_workflow = await get_workflow_by_name(session, name=wf.name)
    if db_workflow:
        raise HTTPException(
            status_code=st.HTTP_302_FOUND,
            detail="Workflow already registered in observe database.",
        )
    return await create_workflow(session=session, workflow=wf)


@workflow.post("/{name}/release", response_model=ReleaseLog)
async def create_workflow_release(
    name: str,
    rl: ReleaseLogCreate,
    session: AsyncSession = Depends(get_async_session),
):
    db_workflow = await get_workflow_by_name(session, name=name)
    if not db_workflow:
        raise HTTPException(
            status_code=st.HTTP_302_FOUND,
            detail="Workflow does not registered in observe database.",
        )
    return await create_release_log(
        session=session,
        workflow_id=db_workflow.id,
        release_log=rl,
    )
