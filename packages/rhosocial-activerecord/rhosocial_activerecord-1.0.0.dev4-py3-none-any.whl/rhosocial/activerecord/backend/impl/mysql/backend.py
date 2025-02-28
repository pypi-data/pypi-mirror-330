import time
from typing import Optional, Tuple, List, Dict

import mysql.connector
from mysql.connector.errors import (
    Error as MySQLError,
    IntegrityError as MySQLIntegrityError,
    ProgrammingError,
    OperationalError as MySQLOperationalError,
    DatabaseError as MySQLDatabaseError,
)

from .dialect import MySQLDialect, SQLDialectBase
from .transaction import MySQLTransactionManager
from ...base import StorageBackend, ColumnTypes
from ...errors import (
    ConnectionError,
    IntegrityError,
    OperationalError,
    QueryError,
    DeadlockError,
    DatabaseError,
    ReturningNotSupportedError
)
from ...typing import QueryResult, ConnectionConfig


class MySQLBackend(StorageBackend):
    """MySQL storage backend implementation"""

    def __init__(self, **kwargs):
        """Initialize MySQL backend

        Args:
            **kwargs: Connection configuration
                - pool_size: Connection pool size
                - pool_name: Pool name for identification
                - Other standard MySQL connection parameters
        """
        super().__init__(**kwargs)
        self._cursor = None
        self._pool = None
        self._transaction_manager = None

        # Configure MySQL specific settings
        if isinstance(self.config, ConnectionConfig):
            self._connection_args = self._prepare_connection_args(self.config)
        else:
            self._connection_args = kwargs

        self._dialect = MySQLDialect(self.config)

    def _prepare_connection_args(self, config: ConnectionConfig) -> Dict:
        """Prepare MySQL connection arguments

        Args:
            config: Connection configuration

        Returns:
            Dict: MySQL connection arguments
        """
        args = config.to_dict()

        # Map config parameters to MySQL connector parameters
        param_mapping = {
            'database': 'database',
            'username': 'user',
            'password': 'password',
            'host': 'host',
            'port': 'port',
            'charset': 'charset',
            'ssl_ca': 'ssl_ca',
            'ssl_cert': 'ssl_cert',
            'ssl_key': 'ssl_key',
            'ssl_mode': 'ssl_mode',
            'pool_size': 'pool_size',
            'pool_name': 'pool_name',
            'auth_plugin': 'auth_plugin'
        }

        connection_args = {}
        for config_key, mysql_key in param_mapping.items():
            if config_key in args:
                connection_args[mysql_key] = args[config_key]

        # Add additional options
        connection_args.update({
            'use_pure': True,  # Use pure Python implementation
            'get_warnings': True,  # Enable warning support
            'raise_on_warnings': False,  # Don't raise on warnings
            'connection_timeout': self.config.pool_timeout,
            'time_zone': self.config.timezone or '+00:00'
        })

        # Add pooling configuration if enabled
        if config.pool_size > 0:
            connection_args['pool_name'] = config.pool_name or 'mysql_pool'
            connection_args['pool_size'] = config.pool_size

        return connection_args

    @property
    def dialect(self) -> SQLDialectBase:
        """Get MySQL dialect"""
        return self._dialect

    def connect(self) -> None:
        """Establish connection to MySQL server

        Original connect method with version cache reset

        Creates a connection pool if pool_size > 0

        Raises:
            ConnectionError: If connection fails
        """
        # Clear version cache on new connection
        if hasattr(self, '_server_version_cache'):
            self._server_version_cache = None

        try:
            if self.config.pool_size > 0:
                # Create connection pool
                if not self._pool:
                    self._pool = mysql.connector.pooling.MySQLConnectionPool(
                        **self._connection_args
                    )
                self._connection = self._pool.get_connection()
            else:
                # Create single connection
                self._connection = mysql.connector.connect(
                    **self._connection_args
                )

            # Configure session
            cursor = self._connection.cursor()
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")
            cursor.execute("SET SESSION sql_mode = 'STRICT_ALL_TABLES'")
            if self.config.timezone:
                cursor.execute(f"SET time_zone = '{self.config.timezone}'")
            cursor.close()

        except MySQLError as e:
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
                if self.transaction_manager.is_active:
                    self.transaction_manager.rollback()
                self._connection.close()
            except MySQLError as e:
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
            self._connection.ping(reconnect=reconnect)
            return True
        except MySQLError:
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
            force_returning: Not used in MySQL

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
            if not self._connection:
                self.connect()

            # Parse statement type
            stmt_type = sql.strip().split(None, 1)[0].upper()
            is_select = stmt_type == "SELECT"
            is_dml = stmt_type in ("INSERT", "UPDATE", "DELETE")
            need_returning = returning and not is_select

            # Check RETURNING support
            if need_returning:
                handler = self.dialect.returning_handler
                if not handler.is_supported:
                    raise ReturningNotSupportedError(
                        "RETURNING clause not supported by MySQL version"
                    )
                # Format and append RETURNING clause
                sql += " " + handler.format_clause(returning_columns)

            # Get or create cursor
            cursor = self._cursor or self._connection.cursor(dictionary=True)

            # Process SQL and parameters
            final_sql, final_params = self.build_sql(sql, params)

            # Convert parameters if needed
            if final_params:
                processed_params = tuple(
                    self.dialect.value_mapper.to_database(value, None)
                    for value in final_params
                )
            else:
                processed_params = None

            # Execute query
            cursor.execute(final_sql, processed_params)

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
                last_insert_id=cursor.lastrowid,
                duration=time.perf_counter() - start_time
            )

            # Auto-commit if not in transaction
            if not self.in_transaction:
                self._connection.commit()

            return result

        except MySQLError as e:
            self._handle_error(e)

    def _handle_error(self, error: Exception) -> None:
        """Handle MySQL specific errors

        Args:
            error: MySQL exception

        Raises:
            Appropriate exception type for the error
        """
        if isinstance(error, MySQLError):
            if isinstance(error, MySQLIntegrityError):
                msg = str(error)
                if "Duplicate entry" in msg:
                    raise IntegrityError(f"Unique constraint violation: {msg}")
                elif "foreign key constraint fails" in msg.lower():
                    raise IntegrityError(f"Foreign key constraint violation: {msg}")
                raise IntegrityError(msg)

            elif isinstance(error, MySQLOperationalError):
                msg = str(error)
                if "Lock wait timeout exceeded" in msg:
                    raise DeadlockError(msg)
                elif "deadlock" in msg.lower():
                    raise DeadlockError(msg)
                raise OperationalError(msg)

            elif isinstance(error, ProgrammingError):
                raise QueryError(str(error))

            elif isinstance(error, MySQLDatabaseError):
                raise DatabaseError(str(error))

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

            # Convert parameters
            converted_params = []
            for params in params_list:
                if params:
                    converted = tuple(
                        self.value_mapper.to_database(value, None)
                        for value in params
                    )
                    converted_params.append(converted)

            cursor.executemany(sql, converted_params)

            # Auto-commit if not in transaction
            if not self.in_transaction:
                self._connection.commit()

            return QueryResult(
                affected_rows=cursor.rowcount,
                duration=time.perf_counter() - start_time
            )

        except MySQLError as e:
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
    def transaction_manager(self) -> MySQLTransactionManager:
        """Get transaction manager"""
        if not self._transaction_manager:
            if not self._connection:
                self.connect()
            self._transaction_manager = MySQLTransactionManager(self._connection)
        return self._transaction_manager

    @property
    def supports_returning(self) -> bool:
        """Check if RETURNING is supported"""
        return self.dialect.returning_handler.is_supported

    def get_server_version(self) -> tuple:
        """Get MySQL server version

        Returns version tuple (major, minor, patch) with caching
        to avoid repeated queries. Version is cached per connection.

        Returns:
            tuple: Server version as (major, minor, patch)
        """
        # Return cached version if available
        if hasattr(self, '_server_version_cache') and self._server_version_cache:
            return self._server_version_cache

        # If we have connection config version, use it
        if hasattr(self.config, 'version') and self.config.version:
            self._server_version_cache = self.config.version
            return self._server_version_cache

        # Otherwise query the server
        try:
            if not self._connection:
                self.connect()

            cursor = self._connection.cursor()
            cursor.execute("SELECT VERSION()")
            version_str = cursor.fetchone()[0]
            cursor.close()

            # Parse version string (e.g. "8.0.26" into (8, 0, 26))
            # Handle also strings like "8.0.26-community" or "5.7.36-log"
            version_parts = version_str.split('-')[0].split('.')
            major = int(version_parts[0])
            minor = int(version_parts[1]) if len(version_parts) > 1 else 0
            patch = int(version_parts[2]) if len(version_parts) > 2 else 0

            # Cache the result
            self._server_version_cache = (major, minor, patch)
            return self._server_version_cache

        except Exception as e:
            # Log the error but don't fail - return a reasonable default
            if hasattr(self, 'logger'):
                self.logger.error(f"Failed to determine MySQL version: {str(e)}")
            # Default to a relatively recent version
            raise Exception(f"Failed to determine MySQL version: {str(e)}")