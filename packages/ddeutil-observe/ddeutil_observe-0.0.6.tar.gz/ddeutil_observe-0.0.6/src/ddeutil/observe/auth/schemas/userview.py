# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .user import UserSchema


class UserView(UserSchema):

    def gen_row(self) -> str:
        """Return a html row value that already map this model attributes.

        :rtype: str
        """
        return (
            f"<td>{self.id}</td>"
            f"<td>{self.username}</td>"
            f"<td>{self.email}</td>"
            f"<td>{self.fullname}</td>"
            f"<td>{self.is_verified}</td>"
        )


class UserJinja(BaseModel):
    username: Optional[str] = None

    @property
    def is_authenticated(self) -> bool:
        return self.username is not None

    @property
    def display_name(self) -> str:
        return self.username
