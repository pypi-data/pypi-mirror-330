# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Header, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from ...auth.deps import required_current_active_user
from ...deps import get_async_session, get_templates
from ...utils import get_logger
from . import crud
from .schemas import (
    WorkflowView,
    WorkflowViews,
)

logger = get_logger("ddeutil.observe")

workflow = APIRouter(
    prefix="/workflow",
    tags=["workflow", "frontend"],
    # NOTE: This page require authentication step first.
    dependencies=[Depends(required_current_active_user)],
)


@workflow.get("/")
async def read_workflows(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    templates: Jinja2Templates = Depends(get_templates),
):
    """Return all workflows."""
    workflows: list[WorkflowView] = WorkflowViews.validate_python(
        await crud.list_workflows(session)
    )
    return templates.TemplateResponse(
        request=request,
        name="workflow/workflow.html",
        context={
            "workflows": workflows,
            "search_text": "",
        },
    )


@workflow.get("/search")
async def search_workflows(
    request: Request,
    search_text: str,
    hx_request: Annotated[Optional[str], Header(...)] = None,
    session: AsyncSession = Depends(get_async_session),
    templates: Jinja2Templates = Depends(get_templates),
):
    workflows: list[WorkflowView] = WorkflowViews.validate_python(
        await crud.search_workflow(session=session, search_text=search_text)
    )
    if hx_request:
        return templates.TemplateResponse(
            request=request,
            name="workflow/partials/workflow_results.html",
            context={"workflows": workflows},
        )
    return templates.TemplateResponse(
        request=request,
        name="workflow/workflow.html",
        context={
            "workflows": workflows,
            "search_text": search_text,
        },
    )


@workflow.get("/logs")
async def read_logs(
    request: Request,
    hx_request: Annotated[Optional[str], Header(...)] = None,
    templates: Jinja2Templates = Depends(get_templates),
):
    """Return all workflows."""
    if hx_request:
        return templates.TemplateResponse(
            "workflow/partials/show_add_author_form.html", {"request": request}
        )
    return templates.TemplateResponse(request=request, name="workflow/log.html")
