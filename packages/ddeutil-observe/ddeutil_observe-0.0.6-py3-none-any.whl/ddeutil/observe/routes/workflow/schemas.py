from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


class WorkflowBase(BaseModel):
    """Base Workflow Pydantic model that does not include surrogate key column
    that create on the observe database.
    """

    name: str
    desc: Optional[str] = None
    params: dict[str, Any]
    on: list[dict[str, Any]]
    jobs: dict[str, Any]


class WorkflowCreate(WorkflowBase): ...


class Workflow(WorkflowBase):
    """Workflow Pydantic model that receive the Workflows model object
    from SQLAlchemy ORM.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    delete_flag: bool
    valid_start: datetime
    valid_end: datetime


class WorkflowView(Workflow):
    model_config = ConfigDict(from_attributes=True)

    def gen_row(self) -> str:
        """Return a html row value that already map this model attributes.

        :rtype: str
        """
        return (
            f"<td>{self.id}</td>"
            f"<td>{self.name}</td>"
            f"<td>{self.params}</td>"
            f"<td>{self.on}</td>"
            f"<td>{self.jobs}</td>"
        )


Workflows = TypeAdapter(list[Workflow])
WorkflowViews = TypeAdapter(list[WorkflowView])


class ReleaseBase(BaseModel):
    """Base Release Pydantic model that does not include surrogate key column
    that create on the observe database.
    """

    release: int


class Release(ReleaseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    workflow_id: int


class LogBase(BaseModel):
    """Base Log Pydantic model that does not include surrogate key column
    that create on the observe database.
    """

    run_id: str
    context: dict[str, Any] = Field(default_factory=dict)


class LogCreate(LogBase): ...


class Log(LogBase):
    model_config = ConfigDict(from_attributes=True)

    release_id: int


class ReleaseLogCreate(ReleaseBase):
    logs: list[LogCreate] = Field(default_factory=list)


class ReleaseLog(ReleaseBase):
    model_config = ConfigDict(from_attributes=True)

    logs: list[Log]
    workflow_id: int
