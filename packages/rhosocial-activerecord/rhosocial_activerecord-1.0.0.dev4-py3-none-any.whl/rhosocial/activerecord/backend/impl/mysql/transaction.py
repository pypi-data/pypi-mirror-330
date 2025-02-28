from typing import Dict
from mysql.connector.errors import Error as MySQLError

from ...errors import TransactionError
from ...transaction import TransactionManager, IsolationLevel


class MySQLTransactionManager(TransactionManager):
    """MySQL transaction manager implementation"""

    # MySQL supported isolation level mappings
    _ISOLATION_LEVELS: Dict[IsolationLevel, str] = {
        IsolationLevel.READ_UNCOMMITTED: "READ UNCOMMITTED",
        IsolationLevel.READ_COMMITTED: "READ COMMITTED",
        IsolationLevel.REPEATABLE_READ: "REPEATABLE READ",  # MySQL default
        IsolationLevel.SERIALIZABLE: "SERIALIZABLE"
    }

    def __init__(self, connection):
        """Initialize MySQL transaction manager

        Args:
            connection: MySQL database connection
        """
        super().__init__()
        self._connection = connection
        self._active_savepoint = None
        self._savepoint_counter = 0

    def _set_isolation_level(self) -> None:
        """Set transaction isolation level

        This is called at the start of each transaction
        """
        if self._isolation_level:
            level = self._ISOLATION_LEVELS.get(self._isolation_level)
            if level:
                try:
                    cursor = self._connection.cursor()
                    cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {level}")
                    cursor.close()
                except MySQLError as e:
                    raise TransactionError(
                        f"Failed to set isolation level to {level}: {str(e)}"
                    )
            else:
                raise TransactionError(
                    f"Unsupported isolation level: {self._isolation_level}"
                )

    def _do_begin(self) -> None:
        """Begin MySQL transaction

        Sets isolation level and starts transaction

        Raises:
            TransactionError: If begin fails
        """
        try:
            # Set isolation level first
            self._set_isolation_level()

            # Start transaction
            self._connection.start_transaction()

        except MySQLError as e:
            raise TransactionError(f"Failed to begin transaction: {str(e)}")

    def _do_commit(self) -> None:
        """Commit MySQL transaction

        Raises:
            TransactionError: If commit fails
        """
        try:
            self._connection.commit()
        except MySQLError as e:
            raise TransactionError(f"Failed to commit transaction: {str(e)}")
        finally:
            self._active_savepoint = None
            self._savepoint_counter = 0

    def _do_rollback(self) -> None:
        """Rollback MySQL transaction

        Raises:
            TransactionError: If rollback fails
        """
        try:
            self._connection.rollback()
        except MySQLError as e:
            raise TransactionError(f"Failed to rollback transaction: {str(e)}")
        finally:
            self._active_savepoint = None
            self._savepoint_counter = 0

    def _generate_savepoint_name(self) -> str:
        """Generate unique savepoint name

        Returns:
            str: Unique savepoint name
        """
        self._savepoint_counter += 1
        return f"SP_{self._savepoint_counter}"

    def _do_create_savepoint(self, name: str) -> None:
        """Create MySQL savepoint

        Args:
            name: Savepoint name

        Raises:
            TransactionError: If create savepoint fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"SAVEPOINT {name}")
            cursor.close()
            self._active_savepoint = name
        except MySQLError as e:
            raise TransactionError(f"Failed to create savepoint {name}: {str(e)}")

    def _do_release_savepoint(self, name: str) -> None:
        """Release MySQL savepoint

        Args:
            name: Savepoint name

        Raises:
            TransactionError: If release savepoint fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"RELEASE SAVEPOINT {name}")
            cursor.close()
            if self._active_savepoint == name:
                self._active_savepoint = None
        except MySQLError as e:
            raise TransactionError(f"Failed to release savepoint {name}: {str(e)}")

    def _do_rollback_savepoint(self, name: str) -> None:
        """Rollback to MySQL savepoint

        Args:
            name: Savepoint name

        Raises:
            TransactionError: If rollback to savepoint fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(f"ROLLBACK TO SAVEPOINT {name}")
            cursor.close()
            if self._active_savepoint == name:
                self._active_savepoint = None
        except MySQLError as e:
            raise TransactionError(
                f"Failed to rollback to savepoint {name}: {str(e)}"
            )

    def supports_savepoint(self) -> bool:
        """Check if savepoints are supported

        Returns:
            bool: Always True for MySQL
        """
        return True

    def get_active_savepoint(self) -> str:
        """Get name of active savepoint

        Returns:
            str: Active savepoint name or None
        """
        return self._active_savepoint

    def clear_active_savepoint(self) -> None:
        """Clear active savepoint reference"""
        self._active_savepoint = None

    @property
    def is_active(self) -> bool:
        """Check if transaction is active

        Returns:
            bool: True if in transaction
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT @@in_transaction")
            result = cursor.fetchone()
            cursor.close()
            return bool(result[0]) if result else False
        except MySQLError:
            return False

    def get_current_isolation_level(self) -> IsolationLevel:
        """Get current transaction isolation level

        Returns:
            IsolationLevel: Current isolation level

        Raises:
            TransactionError: If getting isolation level fails
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT @@transaction_isolation")
            result = cursor.fetchone()
            cursor.close()

            if result:
                # Convert MySQL level name to IsolationLevel enum
                level_name = result[0].upper().replace(' ', '_')
                for isolation_level, mysql_level in self._ISOLATION_LEVELS.items():
                    if mysql_level.upper().replace(' ', '_') == level_name:
                        return isolation_level

            # Default to REPEATABLE READ if not found
            return IsolationLevel.REPEATABLE_READ

        except MySQLError as e:
            raise TransactionError(
                f"Failed to get transaction isolation level: {str(e)}"
            )