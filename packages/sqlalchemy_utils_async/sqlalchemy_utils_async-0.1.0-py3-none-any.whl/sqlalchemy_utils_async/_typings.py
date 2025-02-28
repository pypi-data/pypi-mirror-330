from typing import Union, Any, Sequence
from sqlalchemy.sql._typing import (
    _ColumnExpressionArgument, _ColumnsClauseArgument, _ColumnExpressionOrStrLabelArgument
)
from sqlalchemy.engine.result import _R



WhereClause = _ColumnExpressionArgument[bool]
ColumnsClauseArgument = _ColumnsClauseArgument[Any]
RowDataSequence = Sequence[_R]
RowData = Union[_R|None]
ColumnsOrderByArgument = _ColumnExpressionOrStrLabelArgument[Any]