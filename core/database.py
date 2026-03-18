from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy import func, String, Numeric, Integer, text, Uuid
from core.config import Settings
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Generator
from uuid import UUID, uuid4


name_str = Annotated[str, mapped_column(String(128))]
description = Annotated[str, mapped_column(String(2000),nullable=True)]
int_pk = Annotated[UUID, mapped_column(Uuid, primary_key=True, default=uuid4)]
foreign_uuid = Annotated[UUID, mapped_column(Uuid, nullable=False, default=uuid4)]
slug = Annotated[str, mapped_column(String, nullable=False)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(),onupdate=datetime.now)]
price = Annotated[Decimal, mapped_column(Numeric(10, 2), nullable=False)]
email = Annotated[str, mapped_column(String(255), nullable=False)]
rating = Annotated[float, mapped_column(nullable=False, default=0, server_default=text("0"))]



class Base(AsyncAttrs, DeclarativeBase):
    
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


