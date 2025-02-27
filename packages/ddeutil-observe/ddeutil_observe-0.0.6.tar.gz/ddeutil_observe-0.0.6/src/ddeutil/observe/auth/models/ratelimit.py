# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String

from ...db import Base, Col, Dtype


class Tier(Base):
    __tablename__ = "tier"

    id: Dtype[int] = Col(Integer, primary_key=True)
    name: Dtype[str] = Col(String, nullable=False, unique=True)
    created_at: Dtype[datetime] = Col(
        DateTime(timezone=True),
        default=datetime.now,
        nullable=False,
    )
    updated_at: Dtype[Optional[datetime]] = Col(
        DateTime(timezone=True),
        nullable=True,
    )


class RateLimit(Base):
    __tablename__ = "rate_limit"

    id: Dtype[int] = Col(Integer, primary_key=True)
    tier_id: Dtype[int] = Col(ForeignKey("tier.id"), index=True)
    name: Dtype[str] = Col(String, nullable=False, unique=True)
    path: Dtype[str] = Col(String, nullable=False)
    limit: Dtype[int] = Col(Integer, nullable=False)
    period: Dtype[int] = Col(Integer, nullable=False)

    created_at: Dtype[datetime] = Col(
        DateTime(timezone=True),
        default=datetime.now,
    )
    updated_at: Dtype[Optional[datetime]] = Col(
        DateTime(timezone=True),
        nullable=True,
    )
