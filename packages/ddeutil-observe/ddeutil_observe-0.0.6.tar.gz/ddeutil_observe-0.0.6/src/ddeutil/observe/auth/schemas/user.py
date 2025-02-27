# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional

from fastapi import Form
from pydantic import UUID4, BaseModel, ConfigDict, EmailStr


class UserSchemaBase(BaseModel):
    username: str


class UserDetailSchema(UserSchemaBase):
    email: EmailStr
    fullname: Optional[str] = None


class UserSchema(UserDetailSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    is_verified: bool
    is_active: bool
    is_superuser: bool
    created_at: datetime

    # @field_serializer("id")
    # def serialize_id(self, user_id: UUID4):
    #     return str(user_id)


class UserResetPassForm(UserSchemaBase):
    username: str
    old_password: str
    new_password: str


class UserCreateForm(UserDetailSchema):
    password: str

    # TODO: Move this validation step to client side.
    # @field_validator('password', mode='before')
    # def validate_strong_password(cls, value: str) -> str:
    #     if re.match(
    #         r'((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,64})',
    #         value,
    #     ):
    #         return value
    #     raise ValueError("Password does not strong")


class UserScopeForm(BaseModel):
    scopes_me: bool
    scopes_workflows: bool

    @classmethod
    def as_form(
        cls,
        scopes_me: Annotated[bool, Form()] = False,
        scopes_workflows: Annotated[bool, Form()] = False,
    ):
        return cls(
            scopes_me=scopes_me,
            scopes_workflows=scopes_workflows,
        )

    @property
    def scopes(self) -> list[str]:
        return [
            sc.split("_", maxsplit=1)[-1]
            for sc in self.__dict__
            if sc.startswith("scopes_") and self.__dict__[sc]
        ]
