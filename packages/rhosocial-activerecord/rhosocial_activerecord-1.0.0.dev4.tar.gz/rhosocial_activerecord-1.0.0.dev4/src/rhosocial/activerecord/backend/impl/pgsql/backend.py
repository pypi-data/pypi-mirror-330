import time
from typing import Optional, Tuple, List, Dict, Any

import psycopg
from psycopg import Cursor
from psycopg.errors import (
    Error as PsycopgError,
    IntegrityError as PsycopgIntegrityError,
    OperationalError as PsycopgOperationalError,
    ProgrammingError,
    SerializationFailure,
    DeadlockDetected,
)
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from .dialect import PostgreSQLDialect, SQLDialectBase
from .transaction import PostgreSQLTransactionManager
from ...base import StorageBackend, ColumnTypes
from ...errors import (
    ConnectionError,
    IntegrityError,
    OperationalError,
    QueryError,
    DeadlockError
)
from ...typing import QueryResult, ConnectionConfig


class PostgreSQLBackend(StorageBackend):
    """PostgreSQL storage backend implementation"""

    def __init__(self, **kwargs):
        """Initialize PostgreSQL backend

        Args:
            **kwargs: Connection configuration
                - pool_min: Minimum connections in pool
                - pool_max: Maximum connections in pool
                - Other standard PostgreSQL connection parameters
        """
        super().__init__(**kwargs)
        self._cursor: Optional[Cursor] = None
        self._connection_pool = None
        self._transaction_manager = None
        self._autocommit = True  # Default to autocommit when not in transaction

        # Configure PostgreSQL specific settings
        if isinstance(self.config, ConnectionConfig):
            self._connection_args = self._prepare_connection_args(self.config)
        else:
            self._connection_args = kwargs

        self._dialect = PostgreSQLDialect(self.config)

    def _prepare_connection_args(self, config: ConnectionConfig) -> Dict[str, Any]:
        """Prepare PostgreSQL connection arguments

        Args:
            config: Connection configuration

        Returns:
            Dict[str, Any]: PostgreSQL connection arguments
        """
        args = config.to_dict()

        # Map config parameters to Psycopg3 parameters
        param_mapping = {
            'database': 'dbname',
            'username': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port',
            'pool_size': 'min_size',  # For connection pool
        }

        connection_args = {}
        for config_key, psycopg_key in param_mapping.items():
            if config_key in args:
                connection_args[psycopg_key] = args[config_key]

        # Configure timeouts
        connection_args['connect_timeout'] = config.pool_timeout

        # Set optional SSL parameters
        if config.ssl_ca:
            connection_args['sslmode'] = 'verify-full'
            connection_args['sslcert'] = config.ssl_cert
            connection_args['sslkey'] = config.ssl_key
            connection_args['sslrootcert'] = config.ssl_ca
        elif config.ssl_mode:
            connection_args['sslmode'] = config.ssl_mode

        # Configure connection pool
        if config.pool_size > 0:
            connection_args['min_size'] = max(1, config.pool_size // 2)
            connection_args['max_size'] = config.pool_size

        # Set application name if provided
        if config.pool_name:
            connection_args['application_name'] = config.pool_name

        return connection_args

    @property
    def dialect(self) -> SQLDialectBase:
        """Get PostgreSQL dialect"""
        return self._dialect

    def connect(self) -> None:
        """Establish connection to PostgreSQL server

        Original connect method with version cache reset

        Raises:
            ConnectionError: If connection fails
        """
        # Clear version cache on new connection
        if hasattr(self, '_server_version_cache'):
            self._server_version_cache = None

        try:
            if self.config.pool_size > 0:
                # Create connection pool if not exists
                if not self._connection_pool:
                    # Create connection string
                    conninfo = " ".join(
                        f"{k}={v}" if isinstance(v, str) else f"{k}={str(v)}"
                        for k, v in self._connection_args.items()
                        if v is not None and k not in ('min_size', 'max_size', 'connect_timeout')
                    )

                    # Create connection pool
                    self._connection_pool = ConnectionPool(
                        conninfo=conninfo,
                        min_size=self._connection_args.get('min_size', 1),
                        max_size=self._connection_args.get('max_size', 5),
                        timeout=self._connection_args.get('connect_timeout', 30),
                        open=True  # Automatically open the pool
                    )
                # Get connection from pool
                self._connection = self._connection_pool.getconn()
            else:
                # Create single connection
                self._connection = psycopg.connect(**self._connection_args)

            # Configure connection
            self._connection.row_factory = dict_row

            # Set autocommit mode to match our setting
            # This is just the initial state - will be changed when beginning transactions
            self._connection.autocommit = self._autocommit

            # Set session characteristics
            with self._connection.cursor() as cursor:
                # Set timezone if specified
                if self.config.timezone:
                    cursor.execute(f"SET TIME ZONE '{self.config.timezone}'")
                # Set search path if specified
                if 'search_path' in self._connection_args:
                    cursor.execute(
                        f"SET search_path TO {self._connection_args['search_path']}"
                    )
                # Set statement timeout if specified
                if 'statement_timeout' in self._connection_args:
                    cursor.execute(
                        f"SET statement_timeout = {self._connection_args['statement_timeout']}"
                    )

        except PsycopgError as e:
            raise ConnectionError(f"Failed to connect: {str(e)}")

    def disconnect(self) -> None:
        """Close database connection

        Original disconnect method with version cache reset
        """
        # Clear version cache on disconnect
        if hasattr(self, '_server_version_cache'):
            self._server_version_cache = None

        if self._connection:
            try:
                if self._cursor:
                    self._cursor.close()
                if self.in_transaction:
                    self.rollback_transaction()

                if self._connection_pool:
                    # Return connection to pool
                    self._connection_pool.putconn(self._connection)
                else:
                    # Close single connection
                    self._connection.close()

            except PsycopgError as e:
                raise ConnectionError(f"Failed to disconnect: {str(e)}")
            finally:
                self._connection = None
                self._cursor = None
                self._transaction_manager = None

    def ping(self, reconnect: bool = True) -> bool:
        """Test database connection

        Args:
            reconnect: Whether to attempt reconnection if connection is lost

        Returns:
            bool: True if connection is alive
        """
        if not self._connection:
            if reconnect:
                self.connect()
                return True
            return False

        try:
            # Check connection status
            if self._connection.closed:
                if reconnect:
                    self.connect()
                    return True
                return False

            # Test connection with simple query
            with self._connection.cursor() as cursor:
                cursor.execute("SELECT 1")

            return True

        except PsycopgError:
            if reconnect:
                self.connect()
                return True
            return False

    def execute(
            self,
            sql: str,
            params: Optional[Tuple] = None,
            returning: bool = False,
            column_types: Optional[ColumnTypes] = None,
            returning_columns: Optional[List[str]] = None,
            force_returning: bool = False) -> Optional[QueryResult]:
        """Execute SQL statement

        Args:
            sql: SQL statement
            params: Query parameters
            returning: Whether to return result set
            column_types: Column type mapping
            returning_columns: Specific columns to return
            force_returning: Not used in PostgreSQL (always supported)

        Returns:
            Optional[QueryResult]: Query results

        Raises:
            ConnectionError: Database connection failed
            QueryError: Invalid SQL
            DatabaseError: Other database errors
        """
        start_time = time.perf_counter()

        try:
            # Ensure active connection
            if not self._connection or self._connection.closed:
                self.connect()

            # Parse statement type
            stmt_type = sql.strip().split(None, 1)[0].upper()
            is_select = stmt_type == "SELECT"
            is_dml = stmt_type in ("INSERT", "UPDATE", "DELETE")
            need_returning = returning and is_dml

            # Format RETURNING clause if needed
            if need_returning:
                sql += " " + self.dialect.returning_handler.format_clause(returning_columns)

            # Get or create cursor
            cursor = self._cursor or self._connection.cursor()

            # Process SQL and parameters using builder
            final_sql, final_params = self.build_sql(sql, params)

            # Execute query
            cursor.execute(final_sql, final_params)

            # Handle result set
            data = None
            if returning:
                rows = cursor.fetchall()
                if column_types:
                    # Apply type conversions
                    data = []
                    for row in rows:
                        converted_row = {}
                        for key, value in row.items():
                            db_type = column_types.get(key)
                            if db_type is not None:
                                converted_row[key] = (
                                    self.dialect.value_mapper.from_database(
                                        value, db_type
                                    )
                                )
                            else:
                                converted_row[key] = value
                        data.append(converted_row)
                else:
                    data = rows

            # Build result
            result = QueryResult(
                data=data,
                affected_rows=cursor.rowcount,
                last_insert_id=None,  # PostgreSQL uses RETURNING for this
                duration=time.perf_counter() - start_time
            )

            # Auto-commit if not in transaction
            if not self.in_transaction:
                self._connection.commit()

            return result

        except PsycopgError as e:
            self._handle_error(e)

    def _handle_error(self, error: Exception) -> None:
        """Handle PostgreSQL specific errors

        Args:
            error: PostgreSQL exception

        Raises:
            Appropriate exception type for the error
        """
        if isinstance(error, PsycopgError):
            # Get PostgreSQL error code
            code = getattr(error, 'pgcode', None)

            if isinstance(error, PsycopgIntegrityError):
                msg = str(error)
                if code == '23505':  # unique_violation
                    raise IntegrityError(f"Unique constraint violation: {msg}")
                elif code == '23503':  # foreign_key_violation
                    raise IntegrityError(f"Foreign key constraint violation: {msg}")
                elif code == '23502':  # not_null_violation
                    raise IntegrityError(f"Not null constraint violation: {msg}")
                raise IntegrityError(msg)

            # Handle transaction related errors
            elif isinstance(error, (SerializationFailure, DeadlockDetected)):
                msg = str(error)
                if code == '40P01':  # deadlock_detected
                    raise DeadlockError(msg)
                elif code == '40001':  # serialization_failure
                    raise DeadlockError(msg)
                raise OperationalError(msg)

            elif isinstance(error, PsycopgOperationalError):
                raise OperationalError(str(error))

            elif isinstance(error, ProgrammingError):
                raise QueryError(str(error))

        raise error

    def execute_many(
            self,
            sql: str,
            params_list: List[Tuple]
    ) -> Optional[QueryResult]:
        """Execute batch operations

        Args:
            sql: SQL statement
            params_list: List of parameter tuples

        Returns:
            QueryResult: Execution results
        """
        start_time = time.perf_counter()

        try:
            if not self._connection:
                self.connect()

            cursor = self._cursor or self._connection.cursor()

            # Process SQL (parameters will be processed in executemany)
            final_sql, _ = self.build_sql(sql, params_list[0] if params_list else None)

            # Convert parameters using value mapper
            converted_params = []
            for params in params_list:
                if params:
                    converted = tuple(
                        self.value_mapper.to_database(value, None)
                        for value in params
                    )
                    converted_params.append(converted)

            cursor.executemany(final_sql, converted_params)

            # Auto-commit if not in transaction
            if not self.in_transaction:
                self._connection.commit()

            return QueryResult(
                affected_rows=cursor.rowcount,
                duration=time.perf_counter() - start_time
            )

        except PsycopgError as e:
            self._handle_error(e)

    def begin_transaction(self) -> None:
        """Start transaction"""
        self.transaction_manager.begin()

    def commit_transaction(self) -> None:
        """Commit current transaction"""
        self.transaction_manager.commit()

    def rollback_transaction(self) -> None:
        """Rollback current transaction"""
        self.transaction_manager.rollback()

    @property
    def in_transaction(self) -> bool:
        """Check if in transaction"""
        return self.transaction_manager.is_active

    @property
    def transaction_manager(self) -> PostgreSQLTransactionManager:
        """Get transaction manager"""
        if not self._transaction_manager:
            if not self._connection:
                self.connect()
            self._transaction_manager = PostgreSQLTransactionManager(self._connection)
        return self._transaction_manager

    @property
    def supports_returning(self) -> bool:
        """Check if RETURNING is supported

        Always returns True for PostgreSQL
        """
        return True

    def get_server_version(self) -> tuple:
        """Get PostgreSQL server version

        Returns:
            tuple: Server version as (major, minor, patch)
        """
        if not self._connection or self._connection.closed:
            self.connect()

        try:
            with self._connection.cursor() as cursor:
                cursor.execute("SHOW server_version")
                version_str = cursor.fetchone()['server_version']
                # Parse version string (e.g. "14.5" into (14, 5, 0))
                clean_version = version_str.split()[0]
                parts = clean_version.split('.')
                major = int(parts[0])
                minor = int(parts[1]) if len(parts) > 1 else 0
                patch = int(parts[2]) if len(parts) > 2 else 0
                return major, minor, patch
        except (PsycopgError, ValueError, IndexError):
            # Default to a reasonable version if we can't determine
            return 12, 0, 0