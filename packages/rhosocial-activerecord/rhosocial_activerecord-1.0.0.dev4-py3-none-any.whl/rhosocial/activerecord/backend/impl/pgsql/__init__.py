"""
PostgreSQL backend implementation for the Python ORM.

This module provides a PostgreSQL-specific implementation including:
- PostgreSQL backend with connection management and query execution
- Advanced type mapping and value conversion including native PostgreSQL types
- Transaction management with full ACID compliance and DEFERRABLE support
- PostgreSQL dialect and expression handling
- PostgreSQL-specific type definitions and mappings
"""

from .backend import PostgreSQLBackend
from .dialect import (
    PostgreSQLDialect,
    PostgreSQLExpression,
    PostgreSQLTypeMapper,
    PostgreSQLValueMapper,
)
from .transaction import PostgreSQLTransactionManager
from .types import (
    PostgreSQLTypes,
    PostgreSQLColumnType,
    POSTGRESQL_TYPE_MAPPINGS,
)

__all__ = [
    # Backend
    'PostgreSQLBackend',

    # Dialect related
    'PostgreSQLDialect',
    'PostgreSQLExpression',
    'PostgreSQLTypeMapper',
    'PostgreSQLValueMapper',

    # Transaction
    'PostgreSQLTransactionManager',

    # Types
    'PostgreSQLTypes',
    'PostgreSQLColumnType',
    'POSTGRESQL_TYPE_MAPPINGS',
]