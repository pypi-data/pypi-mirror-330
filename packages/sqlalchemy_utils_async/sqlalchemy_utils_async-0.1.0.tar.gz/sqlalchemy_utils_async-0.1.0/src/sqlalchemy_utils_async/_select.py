from sqlalchemy import select
from sqlalchemy.sql._typing import _ColumnsClauseArgument
from sqlalchemy.ext.asyncio import AsyncSession

def select_one(async_session: AsyncSession, *entities: _ColumnsClauseArgument[Any], **__kw: Any):
    sel = select(*entities, **__kw)
    async_session.scalar(sel)


