import ipaddress
import json
import uuid
from datetime import datetime, date, time
from decimal import Decimal
from typing import Optional, List, Any, Set

from psycopg.types.json import Jsonb
from psycopg.types.range import Range

from .types import POSTGRESQL_TYPE_MAPPINGS
from ...dialect import (
    TypeMapper, ValueMapper, DatabaseType,
    SQLExpressionBase, SQLDialectBase, ReturningClauseHandler, ExplainOptions, ExplainType, ExplainFormat
)
from ...errors import TypeConversionError
from ...helpers import (
    safe_json_dumps, parse_datetime, convert_datetime,
    safe_json_loads
)
from ...typing import ConnectionConfig


class PostgreSQLTypeMapper(TypeMapper):
    """PostgreSQL type mapper implementation"""

    def __init__(self):
        self._placeholder_counter = 0

    def get_column_type(self, db_type: DatabaseType, **params) -> str:
        """Get PostgreSQL column type definition

        Args:
            db_type: Generic database type
            **params: Type parameters (length, precision, etc.)

        Returns:
            str: PostgreSQL column type definition

        Raises:
            ValueError: If type is not supported
        """
        if db_type not in POSTGRESQL_TYPE_MAPPINGS:
            raise ValueError(f"Unsupported type: {db_type}")

        mapping = POSTGRESQL_TYPE_MAPPINGS[db_type]
        if mapping.format_func:
            return mapping.format_func(mapping.db_type, params)
        return mapping.db_type

    def get_placeholder(self, db_type: Optional[DatabaseType] = None) -> str:
        """Get parameter placeholder

        PostgreSQL uses $1, $2, etc. for parameter placeholders

        Returns:
            str: Parameter placeholder ($n)
        """
        self._placeholder_counter += 1
        return f"${self._placeholder_counter}"

    def reset_placeholders(self):
        """Reset placeholder counter"""
        self._placeholder_counter = 0


class PostgreSQLValueMapper(ValueMapper):
    """PostgreSQL value mapper implementation"""

    def __init__(self, config: ConnectionConfig):
        self.config = config
        # Define basic type converters
        self._base_converters = {
            int: int,
            float: float,
            Decimal: str,
            bool: bool,  # PostgreSQL has native boolean
            uuid.UUID: str,
            date: lambda x: convert_datetime(x, format="%Y-%m-%d"),
            time: lambda x: convert_datetime(x, format="%H:%M:%S.%f"),
            datetime: lambda x: convert_datetime(x, timezone=self.config.timezone),
            dict: lambda x: Jsonb(safe_json_dumps(x)),  # Use JSONB by default
            list: lambda x: Jsonb(safe_json_dumps(x)),
            tuple: lambda x: Jsonb(safe_json_dumps(x)),
            ipaddress.IPv4Address: str,
            ipaddress.IPv6Address: str,
            ipaddress.IPv4Network: str,
            ipaddress.IPv6Network: str,
            Range: lambda x: x,  # Native range support
        }

        # Define database type converters
        self._db_type_converters = {
            DatabaseType.BOOLEAN: bool,
            DatabaseType.DATE: lambda v: convert_datetime(v, format="%Y-%m-%d"),
            DatabaseType.TIME: lambda v: convert_datetime(v, format="%H:%M:%S.%f"),
            DatabaseType.DATETIME: lambda v: convert_datetime(v, timezone=self.config.timezone),
            DatabaseType.TIMESTAMP: lambda v: convert_datetime(v, timezone=self.config.timezone),
            DatabaseType.JSON: lambda v: Jsonb(safe_json_dumps(v)),
            DatabaseType.ARRAY: lambda v: v if isinstance(v, list) else [v],
            DatabaseType.UUID: str,
            DatabaseType.DECIMAL: str,
        }

        # Define Python type conversions after database read
        self._from_python_converters = {
            DatabaseType.BOOLEAN: {
                bool: lambda v: v,
                int: bool,
                str: lambda v: v.lower() in ('true', 't', '1', 'yes', 'on'),
            },
            DatabaseType.DATE: {
                date: lambda v: v,
                datetime: lambda v: v.date(),
                str: lambda v: parse_datetime(v).date(),
            },
            DatabaseType.TIME: {
                time: lambda v: v,
                datetime: lambda v: v.time(),
                str: lambda v: parse_datetime(v).time(),
            },
            DatabaseType.DATETIME: {
                datetime: lambda v: v,
                str: lambda v: parse_datetime(v, timezone=self.config.timezone),
                int: lambda v: datetime.fromtimestamp(v),
                float: lambda v: datetime.fromtimestamp(v),
            },
            DatabaseType.TIMESTAMP: {
                datetime: lambda v: v,
                str: lambda v: parse_datetime(v, timezone=self.config.timezone),
                int: lambda v: datetime.fromtimestamp(v),
                float: lambda v: datetime.fromtimestamp(v),
            },
            DatabaseType.JSON: {
                dict: lambda v: v,
                list: lambda v: v,
                str: safe_json_loads,
                Jsonb: lambda v: json.loads(str(v)),
            },
            DatabaseType.ARRAY: {
                list: lambda v: v,
                tuple: list,
                str: safe_json_loads,
            },
            DatabaseType.UUID: {
                uuid.UUID: lambda v: v,
                str: uuid.UUID,
            },
            DatabaseType.DECIMAL: {
                Decimal: lambda v: v,
                str: Decimal,
                int: Decimal,
                float: Decimal,
            },
            DatabaseType.INTEGER: {
                int: lambda v: v,
                str: int,
                float: int,
                bool: int,
            },
            DatabaseType.FLOAT: {
                float: lambda v: v,
                str: float,
                int: float,
            },
            DatabaseType.TEXT: {
                str: lambda v: v,
                int: str,
                float: str,
                bool: str,
                datetime: str,
                date: str,
                time: str,
                uuid.UUID: str,
                Decimal: str,
                ipaddress.IPv4Address: str,
                ipaddress.IPv6Address: str,
                ipaddress.IPv4Network: str,
                ipaddress.IPv6Network: str,
            },
            DatabaseType.BLOB: {
                bytes: lambda v: v,
                bytearray: bytes,
                str: lambda v: v.encode(),
                memoryview: bytes,
            }
        }

    def to_database(self, value: Any, db_type: Optional[DatabaseType] = None) -> Any:
        """Convert Python value to PostgreSQL storage value"""
        if value is None:
            return None

        try:
            # First try basic type conversion
            if db_type is None:
                value_type = type(value)
                if value_type in self._base_converters:
                    return self._base_converters[value_type](value)

            # Then try database type conversion
            if db_type in self._db_type_converters:
                return self._db_type_converters[db_type](value)

            # Special handling for numeric types
            if db_type in (DatabaseType.TINYINT, DatabaseType.SMALLINT,
                           DatabaseType.INTEGER, DatabaseType.BIGINT):
                return int(value)
            if db_type in (DatabaseType.FLOAT, DatabaseType.DOUBLE):
                return float(value)

            # Default to original value
            return value

        except Exception as e:
            raise TypeConversionError(
                f"Failed to convert {type(value)} to {db_type}: {str(e)}"
            )

    def from_database(self, value: Any, db_type: DatabaseType) -> Any:
        """Convert PostgreSQL storage value to Python value"""
        if value is None:
            return None

        try:
            # Get current Python type
            current_type = type(value)

            # Get converter mapping for target type
            type_converters = self._from_python_converters.get(db_type)
            if type_converters:
                # Find converter for current Python type
                converter = type_converters.get(current_type)
                if converter:
                    return converter(value)

                # If no direct converter, try indirect conversion via string
                if current_type != str and str in type_converters:
                    return type_converters[str](str(value))

            # Return original value if no converter found
            return value

        except Exception as e:
            raise TypeConversionError(
                f"Failed to convert PostgreSQL value {value} ({type(value)}) to {db_type}: {str(e)}"
            )


class PostgreSQLExpression(SQLExpressionBase):
    """PostgreSQL expression implementation"""

    def format(self, dialect: SQLDialectBase) -> str:
        """Format PostgreSQL expression"""
        return self.expression


class PostgreSQLReturningHandler(ReturningClauseHandler):
    """PostgreSQL RETURNING clause handler implementation"""

    @property
    def is_supported(self) -> bool:
        """Check if RETURNING clause is supported

        PostgreSQL has always supported RETURNING
        """
        return True

    def format_clause(self, columns: Optional[List[str]] = None) -> str:
        """Format RETURNING clause

        Args:
            columns: Column names to return. None means all columns.

        Returns:
            str: Formatted RETURNING clause
        """
        if not columns:
            return "RETURNING *"

        # Validate and escape each column name
        safe_columns = [self._validate_column_name(col) for col in columns]
        return f"RETURNING {', '.join(safe_columns)}"

    def _validate_column_name(self, column: str) -> str:
        """Validate and escape column name

        Args:
            column: Column name to validate

        Returns:
            str: Escaped column name

        Raises:
            ValueError: If column name is invalid
        """
        # Remove any quotes first
        clean_name = column.strip('"')

        # Basic validation
        if not clean_name or clean_name.isspace():
            raise ValueError("Empty column name")

        # Check for common SQL injection patterns
        dangerous_patterns = [';', '--', 'union', 'select', 'drop', 'delete', 'update']
        lower_name = clean_name.lower()
        if any(pattern in lower_name for pattern in dangerous_patterns):
            raise ValueError(f"Invalid column name: {column}")

        # If name contains special chars, wrap in double quotes
        if ' ' in clean_name or '.' in clean_name or '"' in clean_name:
            return f'"{clean_name}"'

        return clean_name


class PostgreSQLDialect(SQLDialectBase):
    """PostgreSQL dialect implementation"""

    def __init__(self, config: ConnectionConfig):
        """Initialize PostgreSQL dialect

        Args:
            config: Database connection configuration
        """
        # Get version from connection config
        version_str = getattr(config, 'server_version', '9.6.0')
        version = tuple(map(int, version_str.split('.')))
        super().__init__(version)

        # Initialize handlers
        self._type_mapper = PostgreSQLTypeMapper()
        self._value_mapper = PostgreSQLValueMapper(config)
        self._returning_handler = PostgreSQLReturningHandler()

    def format_expression(self, expr: SQLExpressionBase) -> str:
        """Format PostgreSQL expression"""
        if not isinstance(expr, PostgreSQLExpression):
            raise ValueError(f"Unsupported expression type: {type(expr)}")
        return expr.format(self)

    def get_placeholder(self) -> str:
        """Get PostgreSQL parameter placeholder"""
        return self._type_mapper.get_placeholder(None)

    def format_string_literal(self, value: str) -> str:
        """Quote string literal

        PostgreSQL uses single quotes for string literals
        """
        escaped = value.replace("'", "''")
        return f"'{escaped}'"

    def format_identifier(self, identifier: str) -> str:
        """Quote identifier (table/column name)

        PostgreSQL uses double quotes for identifiers
        """
        if '"' in identifier:
            escaped = identifier.replace('"', '""')
            return f'"{escaped}"'
        return f'"{identifier}"'

    def format_limit_offset(self, limit: Optional[int] = None,
                            offset: Optional[int] = None) -> str:
        """Format LIMIT and OFFSET clause"""
        parts = []
        if limit is not None:
            parts.append(f"LIMIT {limit}")
        if offset is not None:
            parts.append(f"OFFSET {offset}")
        return " ".join(parts)

    def get_parameter_placeholder(self, position: int) -> str:
        """Get PostgreSQL parameter placeholder

        PostgreSQL uses $1, $2, etc. based on parameter position
        """
        return "%s"

    def format_explain(self, sql: str, options: Optional[ExplainOptions] = None) -> str:
        """Format PostgreSQL EXPLAIN statement

        Args:
            sql: SQL to explain
            options: EXPLAIN options

        Returns:
            str: Formatted EXPLAIN statement
        """
        if not options:
            options = ExplainOptions()

        explain_options = []

        if options.type == ExplainType.ANALYZE:
            explain_options.append("ANALYZE")

        if options.buffers:
            explain_options.append("BUFFERS")

        if not options.costs:
            explain_options.append("COSTS OFF")

        if options.timing:
            explain_options.append("TIMING")

        if options.verbose:
            explain_options.append("VERBOSE")

        if options.settings:
            explain_options.append("SETTINGS")

        if options.wal:
            explain_options.append("WAL")

        if options.format != ExplainFormat.TEXT:
            explain_options.append(f"FORMAT {options.format.value}")

        if explain_options:
            return f"EXPLAIN ({', '.join(explain_options)}) {sql}"
        return f"EXPLAIN {sql}"

    @property
    def supported_formats(self) -> Set[ExplainFormat]:
        return {ExplainFormat.TEXT, ExplainFormat.JSON, ExplainFormat.YAML, ExplainFormat.XML}

    def create_expression(self, expression: str) -> PostgreSQLExpression:
        """Create PostgreSQL expression"""
        return PostgreSQLExpression(expression)
