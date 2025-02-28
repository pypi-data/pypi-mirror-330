from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import select
from ._typings import WhereClause, ColumnsClauseArgument, ColumnsOrderByArgument
from typing import List, Any
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.engine.result import ScalarResult
from ._typings import RowDataSequence, RowData


def model_manager_maker(engine: AsyncEngine):
    session_maker = async_sessionmaker(engine)

    class _ModelManager:

        @classmethod
        def page_size_to_offset_limit(cls, page: int, size: int) -> (int, int):
            offset = (page - 1) * size
            limit = size
            return offset, limit

        @classmethod
        async def filter(cls,
                         *where_clause: WhereClause,
                         columns_clause: List[ColumnsClauseArgument] = None,
                         page: int = 1,
                         size: int = 25,
                         order_by: List[ColumnsOrderByArgument] = None,
                         ) -> RowDataSequence:
            offset, limit = cls.page_size_to_offset_limit(page, size)
            print('columns_clause', columns_clause)
            if not columns_clause:
                columns_clause = [cls]
            sel = select(*columns_clause).where(*where_clause)

            if order_by is not None:
                sel = sel.order_by(*order_by)

            sel = sel.offset(offset).limit(limit)

            async with session_maker() as session:
                return (await session.scalars(statement=sel)).all()

        @classmethod
        async def get_one(cls,
                          *where_clause: WhereClause,
                          columns_clause: List[ColumnsClauseArgument] = None) -> RowData:
            rows = await cls.filter(
                *where_clause,
                columns_clause=columns_clause,
            )
            if len(rows) == 1:
                return rows[0]
            elif len(rows) == 0:
                return None
            else:
                raise Exception(f"Too many rows returned: {rows}")

    return _ModelManager
